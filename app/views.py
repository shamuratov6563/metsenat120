from rest_framework.views import APIView
from .models import Sponsor, Sponsor_of_Student, Student
from rest_framework.response import Response
from django.db.models import Sum
from rest_framework import serializers
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from .serializers import SponsorSerializer, SponsorDetailSerializer, SponsorCountSerializer, StudentCountSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.db.models.functions import ExtractMonth



class SponsorRegisterAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        full_name = request.data.get('full_name')
        phone_number = request.data.get('phone_number')
        sponsor_type = request.data.get('sponsor_type')
        payment_amount = request.data.get('payment_amount')
        origination_name = request.data.get('origination_name')

        kwargs = {
            'full_name': full_name,
            'phone_number': phone_number,
            'sponsor_type': sponsor_type,
            'payment_amount': payment_amount
        }

        if sponsor_type == 'individual':
            Sponsor.objects.create(
                **kwargs
            )
        else:
            Sponsor.objects.create(
                orgination_name=origination_name,
                **kwargs
            )

        return Response(status=201)


# Studentga sponsor qo'shish
class AddStudentSponsorAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        data = request.data    
        sponsor = data.get("sponsor") # 1
        student = data.get("student") # 2
        allocated_amount = int(data.get("allocated_amount")) # 2000000

        sponsor = Sponsor.objects.get(id=sponsor)
        student = Student.objects.get(id=student)

        # validate data
        # 1. sponsorni puli yetadimi ? (sponsor nechi pul ajratgan shu paytgacha)
        # filter 
        sponsor_allocated_amounts = Sponsor_of_Student.objects.filter(
            sponsor=sponsor).aggregate(
                total_amount=Sum('allocated_amount'))['total_amount'] or 0
        
        active_balance = sponsor.payment_amount - sponsor_allocated_amounts
        
        if active_balance < allocated_amount:
            raise serializers.ValidationError(
                {"error": f"Homiyda yetarli mablag' mavjud emas ({active_balance})"}
                )


        # 2. studentga buncha pul kerakmi ? studentga ajratilgan summa, kerakli summa
        student_received_amount = Sponsor_of_Student.objects.filter(
            student=student).aggregate(
                total_amount=Sum('allocated_amount'))['total_amount'] or 0
        
        student_needed_amount = student.contract_amount - student_received_amount
        if student_needed_amount < allocated_amount:
            raise serializers.ValidationError({"error": f"Talaba uchun bunday kattalikdagi summa ajrata olmaysiz ({student_needed_amount})"})


        Sponsor_of_Student.objects.create(
            sponsor=sponsor, 
            student=student, 
            allocated_amount=allocated_amount
        )
        return Response(status=201)



class SponsorListAPIView(generics.ListAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("full_name", )
    filterset_fields = ('status', )
    

class SponsorDetailAPIView(generics.RetrieveAPIView):
    permission_classes = (permissions.AllowAny, )
    queryset = Sponsor.objects.all()
    serializer_class = SponsorDetailSerializer
    lookup_field = "pk"


class DashboardChartAPIView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request):
        data = []
        # TruncMonth, values 

        sponsors = Sponsor.objects.annotate(month=ExtractMonth('created_at__date')).values('month').annotate(sponsor_count=Count('id')).order_by('month')

        print(SponsorCountSerializer(sponsors, many=True).data)

        students = Student.objects.annotate(month=ExtractMonth('created_at__date')).values('month').annotate(student_count=Count('id')).order_by('month')

        print(StudentCountSerializer(students, many=True).data)



        # group by
        # for i in range(1, 13):
        #     sponsor_count = Sponsor.objects.filter(
        #         created_at__month=i).count()
        #     student_count = Student.objects.filter(
        #         created_at__month=i).count()
        #     data.append({
        #         "month": i,
        #         "student_count": student_count,
        #         "sponsor_count": sponsor_count
        #     })

        return Response(data=data)
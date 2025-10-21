from rest_framework import serializers
from .models import Sponsor
from django.db.models import Sum


class SponsorSerializer(serializers.ModelSerializer):
    spent_amount = serializers.SerializerMethodField()

    def get_spent_amount(self, obj):
        return obj.payment_amounts.aggregate(
            total=Sum('allocated_amount'))['total'] or 0

    class Meta:
        model = Sponsor
        exclude = ("orgination_name", "sponsor_type")


class SponsorDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sponsor
        fields = "__all__" 



class SponsorCountSerializer(serializers.Serializer):
    month = serializers.CharField()
    sponsor_count = serializers.IntegerField()


class StudentCountSerializer(serializers.Serializer):
    month = serializers.CharField()
    student_count = serializers.IntegerField()
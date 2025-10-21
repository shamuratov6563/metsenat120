from django.contrib import admin
from django.urls import path
from app.views import SponsorRegisterAPIView, AddStudentSponsorAPIView, SponsorListAPIView, SponsorDetailAPIView, DashboardChartAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sponsor-register/', SponsorRegisterAPIView.as_view()),
    path('add-student-sponsor/', AddStudentSponsorAPIView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('sponsors/', SponsorListAPIView.as_view()),
    path('sponsors/<int:pk>/', SponsorDetailAPIView.as_view()),
    path('dashboard-chart/', DashboardChartAPIView.as_view())
]


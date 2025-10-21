from django.contrib import admin
from .models import Sponsor, Student, University, Sponsor_of_Student


class SponsorStudentTabularInline(admin.TabularInline):
    extra = 1
    model = Sponsor_of_Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    inlines = [SponsorStudentTabularInline, ]
    list_display = ("id", "full_name", "contract_amount")
    list_display_links = ("id", "full_name")



@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    inlines = [SponsorStudentTabularInline,]
    list_display = ("id", "full_name", "payment_amount")
    list_display_links = ("id", "full_name")

admin.site.register(University)
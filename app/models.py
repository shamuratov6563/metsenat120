from django.db import models


class Sponsor(models.Model):

    class SponsorTypeChoise(models.TextChoices):
        INDIVIDUAL = 'individual', 'Jismoniy shaxs'
        LEGAL = 'legal', 'Yuridik shaxs'

    class StatusSponsorChoise(models.TextChoices):
        NEW = 'new', 'Yangi'
        MODERATION = 'modernation', 'Moderinizatsiya'
        APPROVED = 'approved', 'Tasdiqlangan'
        CANCELLED = 'cancelled', 'Bekor qilingan '
    
    sponsor_type = models.CharField(
        max_length=255,
        choices=SponsorTypeChoise.choices,
        default=SponsorTypeChoise.INDIVIDUAL
    )
    status = models.CharField(
        max_length=255,
        choices=StatusSponsorChoise.choices,
        default=StatusSponsorChoise.NEW
    )
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=13)
    payment_amount = models.PositiveBigIntegerField()
    orgination_name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class University(models.Model):
    name = models.CharField(max_length=255)

class Student(models.Model):
    class DegreeStudentChoice(models.TextChoices):
        BACHELOR = 'bachelor', 'Bakalavr'
        MASTER = 'master', 'Magistr'
    degree_student = models.CharField(
        max_length=255,
        choices=DegreeStudentChoice.choices
    )
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=13)
    contract_amount = models.PositiveBigIntegerField()
    university = models.ForeignKey(
        University,
        related_name='students',
        on_delete=models.PROTECT
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
   
class Sponsor_of_Student(models.Model):
    sponsor = models.ForeignKey(
        Sponsor,
        related_name='payment_amounts',
        on_delete=models.PROTECT
    )

    student = models.ForeignKey(
        Student,
        related_name='allocated_amounts',
        on_delete=models.PROTECT
    )

    allocated_amount = models.BigIntegerField()

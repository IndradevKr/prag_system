from django.db import models
from django.urls import reverse
from schools.models import School, Class
import math

class PhysicalTest(models.Model):
    name = models.CharField(max_length=100, verbose_name="Test Name")
    unit = models.CharField(max_length=20, verbose_name="Unit")
    description = models.TextField(blank=True, verbose_name="Description")

    class Meta:
        verbose_name = "Physical Test"
        verbose_name_plural = "Physical Tests"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.unit})"

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    BMI_CATEGORIES = [
        ('underweight', 'Underweight'),
        ('healthy', 'Healthy'),
        ('overweight', 'Overweight'),
        ('obese', 'Obese'),
    ]

    roll_number = models.CharField(max_length=20, verbose_name="Roll Number")
    name = models.CharField(max_length=100, verbose_name="Full Name")
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='students', verbose_name="Class")
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Gender")
    height = models.FloatField(verbose_name="Height (inches)")
    weight = models.FloatField(verbose_name="Weight (kg)")

    # Calculated fields
    age = models.IntegerField(blank=True, null=True, verbose_name="Age")
    bmi = models.FloatField(blank=True, null=True, verbose_name="BMI")
    bmi_category = models.CharField(max_length=20, choices=BMI_CATEGORIES, blank=True, verbose_name="BMI Category")

    # Performance tracking
    percentile = models.CharField(max_length=50, blank=True, verbose_name="Percentile")
    performance_group = models.IntegerField(blank=True, null=True, verbose_name="Performance Group")
    overall_comment = models.TextField(blank=True, verbose_name="Overall Comment")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        unique_together = ['class_assigned', 'roll_number']
        ordering = ['class_assigned', 'roll_number']

    def __str__(self):
        return f"{self.name} ({self.roll_number})"

    def calculate_age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    def calculate_bmi(self):
        height_m = self.height * 0.0254  # Convert inches to meters
        return round(self.weight / (height_m ** 2), 2)

    def get_bmi_category(self):
        bmi = self.calculate_bmi()
        if bmi < 18.5:
            return 'underweight'
        elif bmi < 25:
            return 'healthy'
        elif bmi < 30:
            return 'overweight'
        else:
            return 'obese'

    def save(self, *args, **kwargs):
        self.age = self.calculate_age()
        self.bmi = self.calculate_bmi()
        self.bmi_category = self.get_bmi_category()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('students:detail', kwargs={'pk': self.pk})

class StudentTestResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='test_results')
    test = models.ForeignKey(PhysicalTest, on_delete=models.CASCADE)
    score = models.FloatField(verbose_name="Score")
    percentile = models.CharField(max_length=50, blank=True, verbose_name="Percentile")
    comment = models.TextField(blank=True, verbose_name="Comment")
    test_date = models.DateField(auto_now_add=True, verbose_name="Test Date")

    class Meta:
        verbose_name = "Test Result"
        verbose_name_plural = "Test Results"
        unique_together = ['student', 'test']
        ordering = ['student', 'test']

    def __str__(self):
        return f"{self.student.name} - {self.test.name}: {self.score}"

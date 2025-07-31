from django.db import models
from django.urls import reverse

# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=200, verbose_name="School Name")
    address = models.TextField(verbose_name="Address")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=15, verbose_name="Phone")
    logo = models.ImageField(upload_to='school_logos/', blank=True, null=True, verbose_name="School Logo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
      verbose_name = "School"
      verbose_name_plural = "Schools"
      ordering = ['name']

    def __str__(self):
      return self.name

    def get_absolute_url(self):
      return reverse('schools:detail', kwargs={'pk': self.pk})

class Class(models.Model):
    GRADE_CHOICES = [
        ('KG', 'Kindergarten'),
        ('1', 'Grade 1'),
        ('2', 'Grade 2'),
        ('3', 'Grade 3'),
        ('4', 'Grade 4'),
        ('5', 'Grade 5'),
        ('6', 'Grade 6'),
        ('7', 'Grade 7'),
        ('8', 'Grade 8'),
        ('9', 'Grade 9'),
        ('10', 'Grade 10'),
    ]

    SECTION_CHOICES = [
        ('A', 'Section A'),
        ('B', 'Section B'),
        ('C', 'Section C'),
        ('D', 'Section D'),
    ]

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classes')
    grade = models.CharField(max_length=10, choices=GRADE_CHOICES, verbose_name="Grade")
    section = models.CharField(max_length=5, choices=SECTION_CHOICES, verbose_name="Section")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
      verbose_name = "Class"
      verbose_name_plural = "Classes"
      unique_together = ['school', 'grade', 'section']
      ordering = ['school', 'grade', 'section']

    def __str__(self):
      return f"{self.school.name} - Grade {self.grade} Section {self.section}"

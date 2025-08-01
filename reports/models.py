from django.db import models
from students.models import Student

class Report(models.Model):
    REPORT_TYPES = [
        ('individual', 'Individual Student Report'),
        ('class', 'Class Report'),
        ('school', 'School Report'),
    ]

    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    generated_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    generated_at = models.DateTimeField(auto_now_add=True)
    file_path = models.FileField(upload_to='reports/', blank=True)

    class Meta:
        ordering = ['-generated_at']

    def __str__(self):
        return f"{self.title} - {self.generated_at.strftime('%Y-%m-%d')}"

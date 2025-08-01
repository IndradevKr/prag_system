from django.contrib import admin
from .models import Student, PhysicalTest, StudentTestResult

@admin.register(PhysicalTest)
class PhysicalTestAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit', 'description']
    search_fields = ['name']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'roll_number', 'class_assigned', 'gender', 'age', 'bmi', 'bmi_category']
    list_filter = ['class_assigned__school', 'class_assigned__grade', 'gender', 'bmi_category']
    search_fields = ['name', 'roll_number']
    readonly_fields = ['age', 'bmi', 'bmi_category']

@admin.register(StudentTestResult)
class StudentTestResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'test', 'score', 'test_date']
    list_filter = ['test', 'test_date']
    search_fields = ['student__name']

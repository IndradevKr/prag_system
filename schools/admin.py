from django.contrib import admin
from .models import School, Class

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'created_at']
    search_fields = ['name', 'email']
    list_filter = ['created_at']

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['school', 'grade', 'section']
    list_filter = ['school', 'grade']
    search_fields = ['school__name']

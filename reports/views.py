from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, FileResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Report
from .utils import generate_individual_report, generate_class_report, generate_school_report, apply_clustering
from students.models import Student
from schools.models import School, Class
import os
from datetime import datetime

class ReportListView(ListView):
    model = Report
    template_name = 'reports/report_list.html'
    context_object_name = 'reports'
    paginate_by = 20

# def generate_report_view(request):
#     if request.method == 'POST':
#         report_type = request.POST.get('report_type')
        
#         try:
#             if report_type == 'individual':
#                 student_id = request.POST.get('student_id')
#                 student = get_object_or_404(Student, pk=student_id)
                
#                 # Generate individual report
#                 file_path = generate_individual_report(student_id)
                
#                 # Create report record
#                 report = Report.objects.create(
#                     title=f"Individual Report - {student.name}",
#                     report_type='individual',
#                     generated_by=request.user if request.user.is_authenticated else None,
#                     file_path=file_path
#                 )
                
#                 messages.success(request, f'Individual report generated successfully for {student.name}!')
                
#             elif report_type == 'class':
#                 class_id = request.POST.get('class_id')
#                 class_obj = get_object_or_404(Class, pk=class_id)
                
#                 # Generate class report
#                 file_path = generate_class_report(class_id)
                
#                 # Create report record
#                 report = Report.objects.create(
#                     title=f"Class Report - {class_obj}",
#                     report_type='class',
#                     generated_by=request.user if request.user.is_authenticated else None,
#                     file_path=file_path
#                 )
                
#                 messages.success(request, f'Class report generated successfully for {class_obj}!')
                
#             elif report_type == 'school':
#                 school_id = request.POST.get('school_id')
#                 school = get_object_or_404(School, pk=school_id)
                
#                 # Generate school report
#                 file_path = generate_school_report(school_id)
                
#                 # Create report record
#                 report = Report.objects.create(
#                     title=f"School Report - {school.name}",
#                     report_type='school',
#                     generated_by=request.user if request.user.is_authenticated else None,
#                     file_path=file_path
#                 )
                
#                 messages.success(request, f'School report generated successfully for {school.name}!')
            
#             return redirect('reports:list')
            
#         except Exception as e:
#             messages.error(request, f'Error generating report: {str(e)}')
    
#     # Get data for form
#     context = {
#         'students': Student.objects.select_related('class_assigned__school').all(),
#         'classes': Class.objects.select_related('school').all(),
#         'schools': School.objects.all(),
#     }
    
#     return render(request, 'reports/generate_report.html', context)

def generate_individual_report_view(request, student_id):
    """Generate individual report directly for a specific student"""
    try:
        student = get_object_or_404(Student, pk=student_id)
        
        # Generate individual report
        file_path = generate_individual_report(student_id)
        
        # Create report record
        report = Report.objects.create(
            title=f"Individual Report - {student.name}",
            report_type='individual',
            generated_by=request.user if request.user.is_authenticated else None,
            file_path=file_path
        )
        
        messages.success(request, f'Individual report generated successfully for {student.name}!')
        
        # Redirect to download the report immediately
        return redirect('reports:download', pk=report.pk)
        
    except Exception as e:
        messages.error(request, f'Error generating report: {str(e)}')
        return redirect('students:detail', pk=student_id)


def generate_report_view(request):
    """Main report generation view"""
    schools = School.objects.all()
    classes = Class.objects.all()
    students = Student.objects.all()

    if request.method == 'POST':
        report_type = request.POST.get('report_type')

        try:
            if report_type == 'individual':
                student_id = request.POST.get('student_id')
                file_path, filename = generate_individual_report(student_id)
                student = Student.objects.get(id=student_id)
                title = f"Individual Report - {student.name}"

            elif report_type == 'class':
                class_id = request.POST.get('class_id')
                file_path, filename = generate_class_report(class_id)
                class_obj = Class.objects.get(id=class_id)
                title = f"Class Report - Grade {class_obj.grade} Section {class_obj.section}"

            elif report_type == 'school':
                school_id = request.POST.get('school_id')
                file_path, filename = generate_school_report(school_id)
                school = School.objects.get(id=school_id)
                title = f"School Report - {school.name}"

            # Save report record
            report = Report.objects.create(
                title=title,
                report_type=report_type,
                generated_by=request.user,
                file_path=f"reports/{filename}"
            )

            messages.success(request, f'Report generated successfully!')

            # Return file for download
            response = FileResponse(
                open(file_path, 'rb'),
                as_attachment=True,
                filename=filename
            )
            return response

        except Exception as e:
            messages.error(request, f'Error generating report: {str(e)}')

    context = {
        'schools': schools,
        'classes': classes,
        'students': students,
    }

    return render(request, 'reports/generate_report.html', context)

def apply_clustering_view(request):
    """Apply K-means clustering to students"""
    if request.method == 'POST':
        try:
            success = apply_clustering()
            if success:
                messages.success(request, 'Student clustering applied successfully!')
            else:
                messages.warning(request, 'Not enough data for clustering (minimum 3 students required)')
        except Exception as e:
            messages.error(request, f'Error applying clustering: {str(e)}')

    return redirect('reports:generate')

def download_report(request, report_id):
    """Download existing report"""
    report = get_object_or_404(Report, id=report_id)
    file_path = os.path.join(settings.MEDIA_ROOT, str(report.file_path))

    if os.path.exists(file_path):
        return FileResponse(
            open(file_path, 'rb'),
            as_attachment=True,
            filename=os.path.basename(file_path)
        )
    else:
        messages.error(request, 'Report file not found')
        return redirect('reports:list')
    
def delete_report(request, pk):
    if request.method == 'POST':
        report = get_object_or_404(Report, pk=pk)
        
        # Delete file if exists
        if report.file_path and os.path.exists(report.file_path.path):
            os.remove(report.file_path.path)
        
        report.delete()
        messages.success(request, 'Report deleted successfully!')
    
    return redirect('reports:list')

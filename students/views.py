from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from .models import Student, PhysicalTest, StudentTestResult
from .forms import StudentForm, ImportStudentsForm
import pandas as pd
from datetime import datetime

class StudentListView(ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    paginate_by = 25

    def get_queryset(self):
        queryset = Student.objects.select_related('class_assigned__school').all()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(roll_number__icontains=search_query) |
                Q(class_assigned__school__name__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context

class StudentDetailView(DetailView):
    model = Student
    template_name = 'students/student_detail.html'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['test_results'] = self.object.test_results.all()
        return context

class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:list')

    def form_valid(self, form):
        messages.success(self.request, 'Student created successfully!')
        return super().form_valid(form)

class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:list')

    def form_valid(self, form):
        messages.success(self.request, 'Student updated successfully!')
        return super().form_valid(form)

def import_students(request):
    if request.method == 'POST':
        form = ImportStudentsForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                excel_file = request.FILES['excel_file']
                school = form.cleaned_data['school']

                # Read Excel file
                df = pd.read_excel(excel_file)

                # Expected columns
                required_columns = ['Roll', 'Name', 'Class', 'Section', 'DOB', 'Gender', 'Height', 'Weight']

                # Check if all required columns exist
                missing_columns = [col for col in required_columns if col not in df.columns]
                if missing_columns:
                    messages.error(request, f'Missing columns: {", ".join(missing_columns)}')
                    return render(request, 'students/import_students.html', {'form': form})

                imported_count = 0
                errors = []

                for index, row in df.iterrows():
                    try:
                        # Get or create class
                        from schools.models import Class
                        class_obj, created = Class.objects.get_or_create(
                            school=school,
                            grade=str(row['Class']),
                            section=str(row['Section']),
                        )

                        # Parse date of birth
                        if isinstance(row['DOB'], str):
                            dob = datetime.strptime(row['DOB'], '%Y-%m-%d').date()
                        else:
                            dob = row['DOB'].date() if hasattr(row['DOB'], 'date') else row['DOB']

                        # Create student
                        student, created = Student.objects.get_or_create(
                            roll_number=str(row['Roll']),
                            class_assigned=class_obj,
                            defaults={
                                'name': str(row['Name']),
                                'date_of_birth': dob,
                                'gender': 'M' if str(row['Gender']).upper().startswith('M') else 'F',
                                'height': float(row['Height']),
                                'weight': float(row['Weight']),
                            }
                        )

                        if created:
                            imported_count += 1

                        # Import physical test data if available
                        test_columns = ['Flamingo Balance', 'Plate Tapping']
                        for test_col in test_columns:
                            if test_col in df.columns and pd.notna(row[test_col]):
                                test, created = PhysicalTest.objects.get_or_create(
                                    name=test_col,
                                    defaults={'unit': 'falls' if 'Flamingo' in test_col else 'seconds'}
                                )

                                StudentTestResult.objects.get_or_create(
                                    student=student,
                                    test=test,
                                    defaults={'score': float(row[test_col])}
                                )

                    except Exception as e:
                        errors.append(f'Row {index + 2}: {str(e)}')

                if imported_count > 0:
                    messages.success(request, f'Successfully imported {imported_count} students!')

                if errors:
                    messages.warning(request, f'Errors encountered: {"; ".join(errors[:5])}')

                return redirect('students:list')

            except Exception as e:
                messages.error(request, f'Error processing file: {str(e)}')
    else:
        form = ImportStudentsForm()

    return render(request, 'students/import_students.html', {'form': form})

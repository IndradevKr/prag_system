from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div, HTML, Row, Column
from .models import Student, PhysicalTest, StudentTestResult

from schools.models import Class  # Import the Class model

class StudentForm(forms.ModelForm):
    class_assigned = forms.ModelChoiceField(
        queryset=Class.objects.all(),
        label='Class',
        empty_label='Select a class',
        required=True
    )

    class Meta:
        model = Student
        fields = ['roll_number', 'name', 'class_assigned', 'date_of_birth', 'gender', 'height', 'weight', 'overall_comment']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'overall_comment': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        # Optional: Filter classes by a specific school if needed
        school = kwargs.pop('school', None)
        super().__init__(*args, **kwargs)
        
        # If a specific school is provided, filter classes
        if school:
            self.fields['class_assigned'].queryset = Class.objects.filter(school=school)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('roll_number', css_class='form-group col-md-6 mb-0'),
                Column('name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('class_assigned', css_class='form-group col-md-4 mb-0'),
                Column('date_of_birth', css_class='form-group col-md-4 mb-0'),
                Column('gender', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('height', css_class='form-group col-md-6 mb-0'),
                Column('weight', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'overall_comment',
            HTML('<br>'),
            Submit('submit', 'Save Student', css_class='btn btn-primary btn-lg')
        )

class ImportStudentsForm(forms.Form):
    excel_file = forms.FileField(
        label='Excel File',
        help_text='Upload an Excel file (.xlsx) with student data'
    )
    school = forms.ModelChoiceField(
        queryset=None,
        label='Select School',
        empty_label='Choose a school...'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from schools.models import School
        self.fields['school'].queryset = School.objects.all()
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.add_input(Submit('submit', 'Import Students', css_class='btn btn-success btn-lg'))

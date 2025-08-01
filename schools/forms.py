from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div, HTML
from .models import School, Class

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'address', 'email', 'phone', 'logo']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Div(
                Field('name', css_class='form-control'),
                Field('address', css_class='form-control'),
                css_class='col-md-6'
            ),
            Div(
                Field('email', css_class='form-control'),
                Field('phone', css_class='form-control'),
                Field('logo', css_class='form-control'),
                css_class='col-md-6'
            ),
            HTML('<br>'),
            Submit('submit', 'Save School', css_class='btn btn-primary btn-lg')
        )
        self.helper.form_class = 'row'

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['school', 'grade', 'section']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Class', css_class='btn btn-primary'))

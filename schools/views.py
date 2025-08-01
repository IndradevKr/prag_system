from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import School, Class
from .forms import SchoolForm, ClassForm

class SchoolListView(ListView):
    model = School
    template_name = 'schools/school_list.html'
    context_object_name = 'schools'
    paginate_by = 10

class SchoolDetailView(DetailView):
    model = School
    template_name = 'schools/school_detail.html'
    context_object_name = 'school'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classes'] = self.object.classes.all()
        return context

class SchoolCreateView(CreateView):
    model = School
    form_class = SchoolForm
    template_name = 'schools/school_form.html'
    success_url = reverse_lazy('schools:list')

    def form_valid(self, form):
        messages.success(self.request, 'School created successfully!')
        return super().form_valid(form)

class SchoolUpdateView(UpdateView):
    model = School
    form_class = SchoolForm
    template_name = 'schools/school_form.html'
    success_url = reverse_lazy('schools:list')

    def form_valid(self, form):
        messages.success(self.request, 'School updated successfully!')
        return super().form_valid(form)

class SchoolDeleteView(DeleteView):
    model = School
    template_name = 'schools/school_confirm_delete.html'
    success_url = reverse_lazy('schools:list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'School deleted successfully!')
        return super().delete(request, *args, **kwargs)

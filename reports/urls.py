from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.ReportListView.as_view(), name='list'),
    path('generate/', views.generate_report_view, name='generate'),
    path('clustering/', views.apply_clustering_view, name='clustering'),
    path('download/<int:report_id>/', views.download_report, name='download'),
     path('<int:pk>/download/', views.download_report, name='download'),
    path('<int:pk>/delete/', views.delete_report, name='delete'),
    path('generate/individual/<int:student_id>/', views.generate_individual_report_view, name='generate_individual'),
]
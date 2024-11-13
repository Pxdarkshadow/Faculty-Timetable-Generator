from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-teacher/', views.add_teacher, name='add_teacher'),
    path('add-subject/', views.add_subject, name='add_subject'),
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('subjects/', views.subject_list, name='subject_list'),
    path('add-timeslot/', views.add_timeslot, name='add_timeslot'),
    path('edit-timeslot/<int:pk>/', views.edit_timeslot, name='edit_timeslot'),
    path('delete-timeslot/<int:pk>/', views.delete_timeslot, name='delete_timeslot'),
    path('timetable/', views.timetable_view, name='timetable_view'),
    path('generate-pdf/<int:teacher_id>/', views.generate_pdf, name='generate_pdf'),
]
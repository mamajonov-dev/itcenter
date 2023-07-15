from django.urls import path

from . import views

urlpatterns = [
    path('group-delete/', views.group_subject_delete, name='group_delete'),
    path('subject-delete/', views.group_subject_delete, name='subject_delete')
]

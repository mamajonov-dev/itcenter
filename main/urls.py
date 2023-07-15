from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),

    path('add-pupil/', views.add_pupil, name='add_pupil'),
    path('add-teacher/', views.add_teacher, name='add_teacher'),
    path('add-group/', views.add_group, name='add_group'),
    path('add-subject/', views.add_subject, name='add_subject'),

    path('pupils/', views.pupils_list, name='pupils_list'),
    path('teachers/', views.teachers_list, name='teachers_list'),
    path('groups/', views.groups_list, name='groups_list'),
    path('subjects/', views.subjects_list, name='subjects_list'),

    path('subject-detail/<str:pk>/', views.subject_detail, name='subject_detail'),
    path('group-detail/<str:pk>/', views.group_detail, name='group_detail'),

    path('update-pupil/<str:pk>/', views.update_pupil, name='update_pupil'),
    path('update-teacher/<str:pk>/', views.update_teacher, name='update_teacher'),
    path('update-subject/<str:pk>/', views.update_subject, name='update_subject'),
    path('update-group/<str:pk>/', views.update_group, name='update_group'),

    path('create-payment/<str:group_id>/<str:pk>/', views.create_payment, name='create_payment'),

    path('paid/', views.paid_pupils, name='paid'),
    path('unpaid/', views.unpaid_pupils, name='unpaid'),

]



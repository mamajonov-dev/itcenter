from django.contrib import admin

from .models import Subject, Teacher, Group, Pupil, Payment


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']
    search_fields = ['name']
    list_filter = ['created', 'updated']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'first_name', 'last_name', 'user']
    list_display_links = ['fullname']
    search_fields = ['fullname']
    list_filter = ['created', 'updated']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'teacher']
    list_display_links = ['name']
    search_fields = ['name', 'subject', 'teacher']
    list_filter = ['created', 'updated']


@admin.register(Pupil)
class PupilAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'group']
    list_display_links = ['first_name']
    search_fields = ['first_name', 'last_name', 'group__name', 'group__teacher__fullname']
    list_filter = ['created', 'updated']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['pupil', 'group', 'month', 'amount']
    list_display_links = ['pupil']
    search_fields = ['pupil__first_name', 'pupil__last_name', 'amount']
    list_filter = ['created', 'updated']

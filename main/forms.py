from django.forms import ModelForm

from .models import Pupil, Teacher, Subject, Group


class PupilForm(ModelForm):
    class Meta:
        model = Pupil
        fields = ['first_name', 'last_name', 'group']
        labels = {
            'group': 'Guruh',
        }

    def __init__(self, *args, **kwargs):
        super(PupilForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update(
                {
                    'class': 'form-control bg-dark text-light',
                }
            )


class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(TeacherForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update(
                {
                    'class': 'form-control bg-dark text-light',
                }
            )


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'subject', 'teacher', 'price']
        labels = {
            "name": "Guruhga nom bering",
            "subject": "Fan nomi",
            "teacher": "Guruh o'qituvchisini tanlang",
            "price": "Oylik to'lovni belgilang"
        }

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update(
                {
                    'class': 'form-control bg-dark text-light',
                }
            )


class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update(
                {
                    'class': 'form-control bg-dark text-light',
                }
            )

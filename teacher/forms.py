from django import forms
from django.contrib.auth.models import User
from . import models
from .models import Teacher

class SubjectForm(forms.ModelForm):
    class Meta:
        model = models.Subject
        fields = '__all__'


class TeacherUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['address', 'mobile', 'profile_pic']


class UpdateTeacherForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']


class TeacherAssForm(forms.ModelForm):
    subjectID = forms.ModelChoiceField(queryset=models.Subject.objects.all(
    ), empty_label="Subject Name", to_field_name="id")

    class Meta:
        model = models.TeacherAssignment
        fields = ['instruction', 'upload']
        widgets = {
            'assignment': forms.Textarea(attrs={'rows': 3, 'cols': 50})
        }

class TeacherAssignForm(forms.ModelForm):
    courseID = forms.ModelChoiceField(queryset=models.Course.objects.all(
    ), empty_label="Course Name", to_field_name="id")

    subjectID = forms.ModelChoiceField(queryset=models.Subject.objects.all(
    ), empty_label="Subject Name", to_field_name="id")

    class Meta:
        model = models.TeacherAssignQuiz
        fields = '__all__'

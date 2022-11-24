from django import forms
from django.contrib.auth.models import User
from . import models
from exam import models as QMODEL
from .models import Teacher


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
    courseID = forms.ModelChoiceField(queryset=models.Course.objects.all(
    ), empty_label="Course Name", to_field_name="id")

    class Meta:
        model = models.TeacherAssignment
        fields = ['instruction', 'upload']
        widgets = {
            'assignment': forms.Textarea(attrs={'rows': 3, 'cols': 50})
        }

class TeacherAssignForm(forms.ModelForm):
    courseID = forms.ModelChoiceField(queryset=models.Course.objects.all(
    ), empty_label="Course Name", to_field_name="id")

    studentID = forms.ModelChoiceField(queryset=models.Student.objects.all(
    ), empty_label="Student Name", to_field_name="id")

    class Meta:
        model = models.TeacherAssignQuiz
        fields = '__all__'

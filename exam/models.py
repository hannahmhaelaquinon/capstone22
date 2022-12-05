from django.db import models
from unittest.util import _MAX_LENGTH
from django.db import models
from .validators import file_size
from django.core.validators import FileExtensionValidator
from student.models import Student
from teacher.models import *

class Levels(models.Model):
    level = models.CharField(max_length=50)

    class meta:
        db_table = 'Level'

class Section(models.Model):
    section = models.CharField(max_length=50)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    level = models.ForeignKey(Levels, on_delete=models.CASCADE)

    class meta:
        db_table = 'Section'



class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    question = models.CharField(max_length=600)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    cat = (('Option1', 'Option1'), ('Option2', 'Option2'),
           ('Option3', 'Option3'), ('Option4', 'Option4'))
    answer = models.CharField(max_length=200, choices=cat)


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)


class Video(models.Model):
    caption = models.CharField(max_length=100)
    video = models.FileField(upload_to="video/%y", validators=[
                             FileExtensionValidator(allowed_extensions=['mp4', 'mkv', 'avi'])])

    def __str__(self):
        return self.caption

    def delete(self, *args, **kwargs):
        self.video.delete()
       # self.cover.delete()
        super().delete(*args, **kwargs)

    class meta:
        db_table = 'Video'


class Library(models.Model):
    title = models.CharField(max_length=100, blank=True)
    subject = models.CharField(max_length=100, blank=True)
    date = models.CharField(max_length=100, blank=True)
    cover = models.ImageField(upload_to='library/image', blank=True)
    pdf = models.FileField(upload_to='library/Files', blank=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        self.cover.delete()
        super().delete(*args, **kwargs)

    class meta:
        db_table = 'Library'

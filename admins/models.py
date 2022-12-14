from django.db import models
from unittest.util import _MAX_LENGTH
from .validators import file_size
from django.core.validators import FileExtensionValidator
from teacher.models import *
from student.models import *


class Section(models.Model):
    section = models.CharField(max_length=50)
    level = models.ForeignKey(Levels, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    
    @property
    def get_name(self):
        return self.level.level
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.level.level

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
        self.cover.delete()
        super().delete(*args, **kwargs)

    class meta:
        db_table = 'Video'


class Library(models.Model):
    title = models.CharField(max_length=100, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    cover = models.ImageField(upload_to='library/image', blank=True)
    pdf = models.FileField(upload_to='library/Files', blank=True)
    
    @property
    def cover_url(self):
        if self.cover and hasattr(self.cover, 'url'):
            return self.cover.url

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        self.cover.delete()
        super().delete(*args, **kwargs)

    class meta:
        db_table = 'Library'

# class Subject(models.Model):
#     name = models.CharField(max_length=50)
#     description
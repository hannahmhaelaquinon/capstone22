from django.db import models
from unittest.util import _MAX_LENGTH
from django.db import models
from .validators import file_size
from django.core.validators import FileExtensionValidator
from student.models import Student
class Course(models.Model):
   course_name = models.CharField(max_length=50)
   question_number = models.PositiveIntegerField()
   total_marks = models.PositiveIntegerField()
   def __str__(self):
        return self.course_name

class Question(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    marks=models.PositiveIntegerField()
    question=models.CharField(max_length=600)
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)
    cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
    answer=models.CharField(max_length=200,choices=cat)

class Result(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    exam = models.ForeignKey(Course,on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)

class Video(models.Model):
    caption = models.CharField(max_length=100)
    video = models.FileField(upload_to="video/%y", validators=[
                             FileExtensionValidator(allowed_extensions=['mp4', 'mkv', 'avi'])])

    def __str__(self):
        return self.caption

class Library(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    booktitle = models.CharField(max_length=150)
    Subject = models.CharField(max_length=150)

class Library1(models.Model):
    Title = models.CharField(max_length=150)
    Subject = models.CharField(max_length=150)
    Date = models.CharField(max_length=150)

    # book_image = models.ImageField(upload_to='image', blank=True)
    # file = mo
    class meta:
        db_table = 'Library'


from django.db import models
from django.contrib.auth.models import User
from exam.models import Course
from exam.models import Student

class Teacher(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/Teacher/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    status= models.BooleanField(default=False)
    salary=models.PositiveIntegerField(null=True)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name

class TeacherAssignment(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    instruction= models.CharField(max_length=500)
    upload =  models.FileField(upload_to='documents/')

class TeacherAssignQuiz(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
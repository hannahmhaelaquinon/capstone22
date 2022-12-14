from django.db import models
from django.contrib.auth.models import User
from teacher.models import *

class Levels(models.Model):
    level = models.CharField(max_length=50)

    def __str__(self):
        return self.level
    
    class meta:
        db_table = 'Level'

class Student(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/Student/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    level = models.ForeignKey(Levels, on_delete=models.CASCADE)
    bmi = models.CharField(max_length=20,null=True,blank=True)
    
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name

class StudentAssSubmit(models.Model):
    #student = models.ForeignKey(Student,on_delete=models.CASCADE)
    #instruction = models.ForeignKey(TeacherAssignment, on_delete=models.CASCADE)
    upload =  models.FileField(upload_to='documents/submission/')
import datetime

from django.db import models
from django.utils import timezone

class Students(models.Model):
	StudentID = models.CharField(max_length=10,default='')
	Name = models.CharField(max_length=30)
	Password = models.CharField(max_length=20)
	CPI = models.FloatField(default=0.00)
	# ResumeLink = models.LinkColumn('item_edit', text='Edit', args=[A('pk')], orderable=False, empty_values=())
	Interests = models.CharField(max_length=40,default='')
	Branch = models.CharField(max_length=20,default='')

class Document(models.Model):
	docfile = models.FileField(upload_to='documents/%Y/%m/%d')
	StudentID = models.CharField(max_length=10,default='')

class Instructors(models.Model):
	InstructorID = models.CharField(max_length=10,default='')
	Name = models.CharField(max_length=30,default='')
	Password = models.CharField(max_length=20,default='')

class AllProjects(models.Model):
	InstructorID = models.ForeignKey(Instructors,on_delete=models.CASCADE)
	ProjectID = models.IntegerField(default=0)
	title = models.CharField(max_length=20,default='')
	description = models.CharField(max_length=200,default='')
	CPIcutoff = models.FloatField(default=0.0)
	max_no_of_students = models.IntegerField(default=0)
	project_status = models.IntegerField(default=1)
	tag = models.CharField(max_length=50,default='')

class AppliedProject(models.Model):
	StudentID = models.ForeignKey(Students,on_delete=models.CASCADE)
	project = models.ForeignKey(AllProjects,on_delete=models.CASCADE)
	time = models.DateTimeField(default=timezone.now)
	allocated = models.IntegerField(default=0)
	accept = models.IntegerField(default=0)

class Chats(models.Model):
	StudentID = models.ForeignKey(Students,on_delete=models.CASCADE)
	InstructorID = models.ForeignKey(Instructors,on_delete=models.CASCADE)

class Message(models.Model):
	MessageID = models.ForeignKey(Chats,on_delete=models.CASCADE)
	SenderID = models.CharField(max_length=10,default='')
	message = models.CharField(max_length=200,default='')
	timestamp = models.DateTimeField(default=timezone.now)

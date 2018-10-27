import datetime

from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Students(models.Model):
	StudentID = models.CharField(max_length=20)
	Name = models.CharField(max_length=30)
	Password = models.CharField(max_length=20)
	CPI = models.CharField(max_length=5,default='0.00')
	# ResumeLink = models.LinkColumn('item_edit', text='Edit', args=[A('pk')], orderable=False, empty_values=())
	Interests = models.CharField(max_length=40,default='')
	Branch = models.CharField(max_length=20,default='')

class Instructors(models.Model):
	InstructorID = models.CharField(max_length=20)
	Name = models.CharField(max_length=30)
	Password = models.CharField(max_length=20)

class AllProjects(models.Model):
	InstructorID = models.ForeignKey(Instructors,on_delete=models.CASCADE)
	StudentID = models.ForeignKey(Students,on_delete=models.CASCADE)
	ProjectID = models.CharField(max_length=20)
	title = models.CharField(max_length=20)
	description = models.CharField(max_length=50)
	CPIcutoff = models.CharField(max_length=5)
	max_no_of_students = models.IntegerField(default=0)
	project_status = models.IntegerField(default=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
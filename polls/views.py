from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict

from .models import Question
from .models import Students
from .models import Instructors
from .models import AllProjects


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})

def login(request):

	# if request.session.get('stud') != None:
	# 	return redirect('polls:student_home')
	# elif request.session.get('inst') != None:
	# 	return redirect('polls:instructor_home')

	if request.method == "POST":

		# if request.POST["type"] == "login":
		userid = request.POST["userid"]
		password = request.POST["password"]

		if Students.objects.filter(StudentID = userid, Password = password).count() > 0:
			# Valid Login/Password
			user = Students.objects.get(StudentID = userid)
			request.session['stud'] = user.StudentID
			return redirect('polls:student_home')
		elif Instructors.objects.filter(InstructorID = userid, Password = password).count() > 0:
			user = Instructors.objects.get(InstructorID = userid)
			request.session['inst'] = user.InstructorID
			return redirect('polls:instructor_home')
		else:
			return render(request, 'polls/login.html')
	else:
		return render(request, 'polls/login.html')

def student_home(request):
	if request.session.get('stud') != None:

		student_id = request.session['stud']
		student = Students.objects.get(StudentID=student_id)
		student = model_to_dict(student)
		# print(student_cpi)
		
		project_list = AllProjects.objects.filter(CPIcutoff__lte = student['CPI'] )

		# resume_list = Resume.objects.filter(user = user).order_by("-timestamp")

		# if request.session.get('resume_id') != None:
		# 	del request.session['resume_id']

		# request_list = Request.objects.filter(user_receiver = user)

		# notifications = Notification.objects.filter(user_receiver = user)

		return render(request, 'polls/student_home.html', {'project_list':project_list})

	else:

		return redirect('polls:login')
def results(request):
    response = "You're looking at the results of question."
    return HttpResponse(response)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

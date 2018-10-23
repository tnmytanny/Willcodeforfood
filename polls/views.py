from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect

from .models import Question
from .models import Students


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
	if request.method == "POST":

		# if request.POST["type"] == "login":

		userid = request.POST["userid"]
		password = request.POST["password"]

		if Students.objects.filter(StudentID = userid, Password = password).count() > 0:

			# Valid Login/Password

			user = Students.objects.get(StudentID = userid)

			request.session['user'] = user.StudentID

			return redirect('polls:home')

		else:

			return render(request, 'polls/login.html')
	else:
		return render(request, 'polls/login.html')
def results(request):
    response = "You're looking at the results of question."
    return HttpResponse(response)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

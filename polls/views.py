from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict
from django.utils import timezone
from django.db.models import Max
from .models import Question
from .models import Students
from .models import Instructors
from .models import AllProjects
from .models import UpdatedProject
from .models import Message
from .models import Chats

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

	if request.session.get('stud') != None:
		return redirect('polls:student_home')
	elif request.session.get('inst') != None:
		return redirect('polls:instructor_home')

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
		student1 = Students.objects.get(StudentID=student_id)
		student = model_to_dict(student1)
		# print(student_cpi)
		
		project_list = AllProjects.objects.filter(CPIcutoff__lte = student['CPI'], project_status=1)
		applied_projects = UpdatedProject.objects.values_list('project',flat=True).filter(StudentID__StudentID=student_id,project__project_status=1)
		# applied_projects = model_to_dict(applied_projects)
		project2=[]
		for i in applied_projects:
			temp_proj = AllProjects.objects.get(pk=i)
			project2.append(temp_proj)
		print(project2)
		project_list = set(project_list).difference(set(project2))
		applied_projects = UpdatedProject.objects.values_list('project',flat=True).filter(StudentID__StudentID=student_id,project__project_status=1,accept=0)
		# applied_projects = model_to_dict(applied_projects)
		project2=[]
		for i in applied_projects:
			temp_proj = AllProjects.objects.get(pk=i)
			project2.append(temp_proj)
		# resume_list = Resume.objects.filter(user = user).order_by("-timestamp")
		# if request.session.get('resume_id') != None:
		# 	del request.session['resume_id']
		# request_list = Request.objects.filter(user_receiver = user)
		# notifications = Notification.objects.filter(user_receiver = user)

		return render(request, 'polls/student_home.html', {'project_list':project_list,'project2':project2,'change_pass':0})
	else:
		return redirect('polls:login')

def student_project_detail(request):
	if request.method == "POST":
		project_id = request.POST["projectid"]
		instructor_id = request.POST["instructorid"]
		project = AllProjects.objects.get(ProjectID=project_id, InstructorID__InstructorID=instructor_id)
		# print(model_to_dict(project))
		return render(request, 'polls/student_project_detail.html',{'project':project})
	else:
		return redirect('polls:student_home')

def student_project_apply(request):
	if request.method == "POST":
		project_id = request.POST["projectid"]
		instructor_id = request.POST["instructorid"]
		student_id = request.session['stud']
		student = Students.objects.get(StudentID=student_id)
		project = AllProjects.objects.get(ProjectID=project_id, InstructorID__InstructorID=instructor_id)
		project2 = UpdatedProject(StudentID=student,project=project,time=timezone.now())
		project2.save()
		# request.session["applied"] = 1
		# print(model_to_dict(project))
	return redirect('polls:student_home')

def student_project_cancel(request):
	if request.method == "POST":
		project_id = request.POST["projectid"]
		instructor_id = request.POST["instructorid"]
		student_id = request.session['stud']
		student = Students.objects.get(StudentID=student_id)
		project = AllProjects.objects.get(ProjectID=project_id, InstructorID__InstructorID=instructor_id)
		UpdatedProject.objects.get(StudentID=student,project=project).delete()
		# project2.save()
		# request.session["applied"] = 1
		# print(model_to_dict(project))
	return redirect('polls:student_home')

def student_allocated_projects(request):
	if request.session.get('stud') != None:
		student_id = request.session['stud']

		Allocated_projects_pending = UpdatedProject.objects.filter(StudentID__StudentID = student_id, allocated = 1, accept = 0)
		Allocated_projects_accepted = UpdatedProject.objects.filter(StudentID__StudentID = student_id, allocated = 1, accept = 1)
		return render(request, 'polls/student_allocated_projects.html', {'Allocated_projects_pending':Allocated_projects_pending, 'Allocated_projects_accepted':Allocated_projects_accepted})
	else:
		return redirect('polls:student_home')

def student_project_accept(request):
	if request.method == "POST":
		student_id = request.session['stud']
		project_id = request.POST["projectid"]
		instructor_id = request.POST["instructorid"]
		print(student_id)
		print(project_id)
		print(instructor_id)
		UpdatedProject.objects.filter(StudentID__StudentID = student_id, project__ProjectID = project_id, project__InstructorID__InstructorID = instructor_id).update(accept = 1)
		# project2.save()
		# print(project2)
		return redirect('polls:student_allocated_projects')
	else:
		return redirect('polls:student_allocated_projects')

def student_project_reject(request):
	if request.method == "POST":
		student_id = request.session['stud']
		project_id = request.POST["projectid"]
		instructor_id = request.POST["instructorid"]
		UpdatedProject.objects.filter(StudentID__StudentID = student_id, project__ProjectID = project_id, project__InstructorID__InstructorID = instructor_id).delete()
		return redirect('polls:student_allocated_projects')
	else:
		return redirect('polls:student_allocated_projects')

def student_filter_project(request):
	if request.method == "POST":
		filter_tag = request.POST["filter_tag"]
		student_id = request.session['stud']
		student1 = Students.objects.get(StudentID=student_id)
		student = model_to_dict(student1)
		# print(student_cpi)
		
		project_list = AllProjects.objects.filter(CPIcutoff__lte = student['CPI'], project_status=1,tag__contains=filter_tag)
		applied_projects = UpdatedProject.objects.values_list('project',flat=True).filter(StudentID__StudentID=student_id,project__project_status=1)
		# applied_projects = model_to_dict(applied_projects)
		project2=[]
		for i in applied_projects:
			temp_proj = AllProjects.objects.get(pk=i)
			project2.append(temp_proj)
		print(project2)
		project_list = set(project_list).difference(set(project2))
		applied_projects = UpdatedProject.objects.values_list('project',flat=True).filter(StudentID__StudentID=student_id,project__project_status=1,accept=0,project__tag__contains=filter_tag)
		# applied_projects = model_to_dict(applied_projects)
		project2=[]
		for i in applied_projects:
			temp_proj = AllProjects.objects.get(pk=i)
			project2.append(temp_proj)
		# resume_list = Resume.objects.filter(user = user).order_by("-timestamp")
		# if request.session.get('resume_id') != None:
		# 	del request.session['resume_id']
		# request_list = Request.objects.filter(user_receiver = user)
		# notifications = Notification.objects.filter(user_receiver = user)

		return render(request, 'polls/student_home.html', {'project_list':project_list,'project2':project2})
	else:
		return redirect('polls:login')

def student_create_chat(request):
	if request.method == "POST":
		student_id = request.session['stud']
		#project_id = request.POST["projectid"]
		instructor_id = request.POST["instructorid"]
		student = Students.objects.get(StudentID=student_id)
		instructor = Instructors.objects.get(InstructorID=instructor_id)
		already_chat = Chats.objects.filter(StudentID=student,InstructorID=instructor)
		print(already_chat)
		if not already_chat:
			chat = Chats(StudentID=student,InstructorID=instructor)
			print("hey",chat)
			chat.save()
	return redirect('polls:student_home')

def student_show_messages(request):
	if request.method == "POST":
		student_id = request.session['stud']
		chat = Chats.objects.filter(StudentID__StudentID=student_id)
		return render(request,'polls/student_show_messages.html',{'chat':chat})
	else:
		return redirect('polls:student_home')

def chat_detail(request):
	if request.method == "POST":
		if request.session.get('stud') != None:
			student_id = request.session["stud"]
			instructor_id = request.POST["instructorid"]
			login_id = request.POST["loginid"]
			print(instructor_id)
			print(student_id)
			print(login_id)
			
			chat = Chats.objects.get(StudentID__StudentID=student_id,InstructorID__InstructorID=instructor_id)
			message = Message.objects.filter(MessageID=chat)
			return render(request,'polls/chat_detail.html',{'message':message,'loginid':login_id,'instructorid':instructor_id,'studentid':student_id})
		elif request.session.get('inst') != None:
			return redirect('polls:instructor_home')
	else:
		return redirect('polls:login')

def send_message(request):
	if request.method == "POST":
		message = request.POST["message"]
		student_id = request.POST["studentid"]
		instructor_id = request.POST["instructorid"]
		sender = request.POST["sender"]
		print(sender)
		print(student_id)
		print(instructor_id)
		Message_ID = Chats.objects.get(StudentID__StudentID=student_id,InstructorID__InstructorID=instructor_id)
		chat = Message(MessageID=Message_ID,SenderID=sender,message=message,timestamp=timezone.now())
		print(Message_ID)
		chat.save()
		mychat = Chats.objects.get(StudentID__StudentID=student_id,InstructorID__InstructorID=instructor_id)
		message = Message.objects.filter(MessageID=mychat)
		return render(request,'polls/chat_detail.html',{'message':message,'loginid':sender,'instructorid':instructor_id,'studentid':student_id})
	else :
		return redirect('polls:login')

def change_password(request):
	if request.method == "POST":
		if request.session.get('inst') != None:
			instructor_id = request.session['inst']
			oldpass = request.POST["oldpass"]
			newpass = request.POST["newpass"]
			newpassagain = request.POST["newpassagain"]
			change_pass=2
			instructor1 = Instructors.objects.filter(InstructorID=instructor_id,Password=oldpass)
			if(newpassagain==newpass and instructor1):
				Instructors.objects.filter(InstructorID=instructor_id,Password=oldpass).update(Password=newpass)
				change_pass=1
			project_list = AllProjects.objects.filter(InstructorID__InstructorID = instructor_id,project_status=1)
			return render(request, 'polls/instructor_home.html', {'project_list':project_list,'instructor_id':instructor_id,'change_pass':change_pass})#,'project2':project2})
		elif request.session.get('stud') != None:
			student_id = request.session['stud']
			oldpass = request.POST["oldpass"]
			newpass = request.POST["newpass"]
			newpassagain = request.POST["newpassagain"]
			change_pass=2
			student1 = Students.objects.get(StudentID=student_id)
			student = model_to_dict(student1)
			project_list = AllProjects.objects.filter(CPIcutoff__lte = student['CPI'], project_status=1)
			applied_projects = UpdatedProject.objects.values_list('project',flat=True).filter(StudentID__StudentID=student_id,project__project_status=1)
			project2=[]
			for i in applied_projects:
				temp_proj = AllProjects.objects.get(pk=i)
				project2.append(temp_proj)
			print(project2)
			project_list = set(project_list).difference(set(project2))
			applied_projects = UpdatedProject.objects.values_list('project',flat=True).filter(StudentID__StudentID=student_id,project__project_status=1,accept=0)
			# applied_projects = model_to_dict(applied_projects)
			project2=[]
			for i in applied_projects:
				temp_proj = AllProjects.objects.get(pk=i)
				project2.append(temp_proj)
			# resume_list = Resume.objects.filter(user = user).order_by("-timestamp")
			student1 = Students.objects.filter(StudentID=student_id,Password=oldpass)
			if(newpassagain==newpass and student1):
				Students.objects.filter(StudentID=student_id,Password=oldpass).update(Password=newpass)
				change_pass=1
			return render(request, 'polls/student_home.html', {'project_list':project_list,'project2':project2,'change_pass':change_pass})
	else:
		return redirect('polls:login')

# def student_inst_chat(request):
# 	if request.method == "POST":
# 		student_id = request.session['stud']
# 		#project_id = request.POST["projectid"]
# 		instructor_id = request.POST["instructorid"]
# 		messages = Message.objects.filter(StudentID=student_id, InstructorID__InstructorID=instructor_id)
# 		#UpdatedProject.objects.filter(StudentID__StudentID = student_id, project__ProjectID = project_id, project__InstructorID__InstructorID = instructor_id).delete()
# 		return render(request,'polls/student_instructor_chat.html',{'messages':messages,'student_id':student_id,'instructor_id':instructor_id})
# 	else:
# 		return render(request,'polls/student_instructor_chat.html')

# def student_new_message(request):
# 	if request.method == "POST":
# 		student_id = request.session['stud']
# 		student1 = Students.objects.get(StudentID=student_id)
# 		#project_id = request.POST["projectid"]
# 		instructor_id = request.POST["instructorid"]
# 		instructor1 = Instructors.objects.get(InstructorID=instructor_id)
# 		message = request.POST["message"]
# 		#timestamp = request.POST["timestamp"]
# 		#print (message)
# 		message = Message(InstructorID=instructor1, StudentID=student1,SenderID=student_id,ReceiverID=instructor_id,message=message)
# 		message.save()
# 		messages = Message.objects.filter(StudentID=student_id, InstructorID__InstructorID=instructor_id)
# 		#m1 = model_to_dict(messages)
# 		#print (m1)
# 		return render(request,'polls/student_instructor_chat.html',{'messages':messages,'student_id':student_id,'instructor_id':instructor_id})#,{'instructorid':instructor_id})#,{'messages':messages,'student_id':student_id.StudentID})
# 	else:
# 		return render(request,'polls/student_instructor_chat.html')

def instructor_home(request):
	if request.session.get('inst') != None:

		instructor_id = request.session['inst']
		instructor1 = Instructors.objects.get(InstructorID=instructor_id)
		instructor = model_to_dict(instructor1)
		# print(student_cpi)
		
		project_list = AllProjects.objects.filter(InstructorID__InstructorID = instructor['InstructorID'],project_status=1)#, project_status=1)
		#applied_projects = UpdatedProject.objects.values_list('project',flat=True).filter(StudentID__StudentID=instructor_id)
		# applied_projects = model_to_dict(applied_projects)
		#project2=[]
		#for i in applied_projects:
		#	temp_proj = AllProjects.objects.get(pk=i)
		#	project2.append(temp_proj)
		#print(project2)
		
		#project_list = set(project_list).difference(set(project2))
		
		# resume_list = Resume.objects.filter(user = user).order_by("-timestamp")
		# if request.session.get('resume_id') != None:
		# 	del request.session['resume_id']
		# request_list = Request.objects.filter(user_receiver = user)
		# notifications = Notification.objects.filter(user_receiver = user)

		return render(request, 'polls/instructor_home.html', {'project_list':project_list,'instructor_id':instructor_id,'change_pass':0})#,'project2':project2})
	else:
		return redirect('polls:login')

def instructor_project_detail(request):
	if request.method == "POST":
		status = request.POST["status"]
		project_id = request.POST["projectid"]
		
		instructor_id = request.session['inst']
		# instructor1 = Instructors.objects.get(InstructorID=instructor_id)
		# instructor_id = instructor1['InstructorID']
		#instructor_id = request.POST["instructorid"]
		project = AllProjects.objects.get(ProjectID=project_id, InstructorID__InstructorID=instructor_id)
		show_applied = 1
		if status=='1':
			studentid=request.POST["studentid"]
			# print("kajskas",studentid)
			result = UpdatedProject.objects.filter(project=project, StudentID__StudentID=studentid).update(allocated=1)
			# print("jkdfd",result)
		elif status=='2':
			studentid=request.POST["studentid"]
			UpdatedProject.objects.filter(StudentID__StudentID = studentid, project = project).delete()
		elif status=='3':
			show_applied = 0
		list_of_students_applied = UpdatedProject.objects.filter(project=project)
		los_allocated = UpdatedProject.objects.filter(project=project,allocated=1,accept=0)
		los_selected = UpdatedProject.objects.filter(project=project,allocated=1,accept=1)
		los_applied = set(list_of_students_applied).difference(set(los_allocated)).difference(set(los_selected))
		# print(model_to_dict(project))
		return render(request, 'polls/instructor_project_detail.html',{'show_applied':show_applied,'project':project,'applied':los_applied,'allocated':los_allocated,'selected':los_selected})
	else:
		return redirect('polls:instructor_home')

def instructor_project_edit(request):
	if request.method == "POST":
		project_id = request.POST["projectid"]
		instructor_id = request.POST["instructorid"]
		project = AllProjects.objects.get(ProjectID=project_id, InstructorID__InstructorID=instructor_id)
		# print(model_to_dict(project))
		return render(request, 'polls/instructor_project_edit.html',{'project':project})
	else:
		return redirect('polls:instructor_home')

# def instructor_project_delete(request):
# 	if request.method == "POST":
# 		project_id = request.POST["projectid"]
# 		instructor_id = request.POST["instructorid"]
# 		project = AllProjects.objects.get(ProjectID=project_id, InstructorID__InstructorID=instructor_id)
# 		# print(model_to_dict(project))
# 		return render(request, 'polls/instructor_project_delete.html',{'project':project})
# 	else:
# 		return redirect('polls:instructor_home')

def instructor_project_delete(request):
	if request.method == "POST":
		project_id = request.POST["projectid"]
		instructor_id = request.POST["instructorid"]
		# instructor1 = Instructors.objects.get(InstructorID=instructor_id)
		#title = request.POST["title"]
		#description = request.POST["description"]
		#CPIcutoff = request.POST["CPIcutoff"]
		#max_no_of_students = request.POST["max_no_of_students"]
		project = AllProjects.objects.get(ProjectID=project_id, InstructorID__InstructorID=instructor_id)
		#project.InstructorID=instructor1
		#project.description=description
		#project.title=title
		#project.CPIcutoff=CPIcutoff
		#project.max_no_of_students=max_no_of_students
		project2 = UpdatedProject.objects.filter(project=project)
		project.delete()
		project2.delete()
		# print(model_to_dict(project))
		return redirect('polls:instructor_home')
	else:
		return redirect('polls:instructor_home')

def instructor_project_close(request):
	if request.method == "POST":
		project_id = request.POST["projectid"]
		instructor_id = request.POST["instructorid"]
		project = AllProjects.objects.filter(ProjectID=project_id, InstructorID__InstructorID=instructor_id).update(project_status=0)
		project2 = UpdatedProject.objects.filter(project=project,accept=0).delete()
		return redirect('polls:instructor_home')
	else:
		return redirect('polls:instructor_home')

def instructor_project_change(request):
	if request.method == "POST":
		project_id = request.POST["projectid"]
		instructor_id = request.POST["instructorid"]
		instructor1 = Instructors.objects.get(InstructorID=instructor_id)
		title = request.POST["title"]
		tag=request.POST["tags"]
		description = request.POST["description"]
		CPIcutoff = request.POST["CPIcutoff"]
		max_no_of_students = request.POST["max_no_of_students"]
		project = AllProjects.objects.get(ProjectID=project_id, InstructorID__InstructorID=instructor_id)
		project.InstructorID=instructor1
		project.description=description
		project.tag=tag
		AllProjects.objects.filter(ProjectID=project_id, InstructorID__InstructorID=instructor_id).update(description = description,CPIcutoff=CPIcutoff,max_no_of_students=max_no_of_students,tag=tag)
		# project.InstructorID=instructor1
		# project.description='testing'
		#project.title=title
		# project.CPIcutoff=CPIcutoff
		# project.max_no_of_students=max_no_of_students
		# project.save()
		# print(model_to_dict(project))
		return redirect('polls:instructor_home')
	else:
		return redirect('polls:instructor_home')

def instructor_new_project(request):
	if request.method == "POST":
		#project_id = request.POST["projectid"]
		instructor_id = request.POST["instructorid"]
		#project = AllProjects.objects.get(ProjectID=project_id, InstructorID__InstructorID=instructor_id)
		# print(model_to_dict(project))
		return render(request, 'polls/instructor_new_project.html',{'instructor_id':instructor_id})
	else:
		return redirect('polls:instructor_home')

def instructor_project_create(request):
	if request.method == "POST":
		instructor_id = request.POST["instructorid"]
		instructor1 = Instructors.objects.get(InstructorID=instructor_id)
		project_id = AllProjects.objects.values_list('ProjectID','InstructorID').filter(InstructorID__InstructorID=instructor_id).aggregate(Max('ProjectID'))
		# print(project_id)
		title = request.POST["title"]
		tag = request.POST["tags"]
		description = request.POST["description"]
		CPIcutoff = request.POST["CPIcutoff"]
		max_no_of_students = request.POST["max_no_of_students"]
		projectid = project_id['ProjectID__max']
		print(project_id["ProjectID__max"])
		if projectid==None:
			projectid = 1
		else:
			projectid = projectid + 1
		print(projectid)
		project = AllProjects(InstructorID=instructor1,ProjectID=projectid, title=title,description=description,CPIcutoff=CPIcutoff,max_no_of_students=max_no_of_students,tag=tag)
		project.save()

	return redirect('polls:instructor_home')

def instructor_allocated_projects(request):
	if request.session.get('inst') != None:
		instructor_id = request.session['inst']

		# Allocated_projects_pending = UpdatedProject.objects.filter(StudentID__StudentID = student_id, allocated = 1, accept = 0)
		Allocated_projects_accepted = AllProjects.objects.filter(InstructorID__InstructorID = instructor_id, project_status=0)
		print(instructor_id)
		return render(request, 'polls/instructor_allocated_projects.html', {'Allocated_projects_accepted':Allocated_projects_accepted})
	else:
		return redirect('polls:login')

# def instructor_add_project(request):
# 	if request.method == "POST":
# 		#project_id = request.POST["projectid"]
# 		instructor_id = request.POST["instructorid"]
# 		instructor1 = Instructors.objects.get(InstructorID=instructor_id)
# 		title = request.POST["title"]
# 		description = request.POST["description"]
# 		CPIcutoff = request.POST["CPIcutoff"]
# 		max_no_of_students = request.POST["max_no_of_students"]
# 		###How to add project id??
# 		project = AllProjects(InstructorID=instructor1, title=title,description=description,CPIcutoff=CPIcutoff,max_no_of_students=max_no_of_students)
# 		project.save()
# 		# print(model_to_dict(project))
# 		return render(request, 'polls/instructor_home.html')
# 	else:
# 		return redirect('polls:instructor_home')

def logout(request):
	request.session.flush()

	return redirect('polls:login')

def results(request):
    response = "You're looking at the results of question."
    return HttpResponse(response)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    # ex: /polls/
    path('myindex/', views.index, name='index'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('', views.login, name='login'),
    path('student_home/', views.student_home, name='student_home'),
    path('student_project_detail/', views.student_project_detail, name='student_project_detail'),
    path('student_project_apply/', views.student_project_apply, name='student_project_apply'),
    path('student_project_cancel/', views.student_project_cancel, name='student_project_cancel'),
    path('student_allocated_projects/', views.student_allocated_projects, name='student_allocated_projects'),
    path('student_project_accept/', views.student_project_accept, name='student_project_accept'),
    path('student_project_reject/', views.student_project_reject, name='student_project_reject'),
    path('student_inst_chat/', views.student_inst_chat, name='student_inst_chat'),
    path('student_new_message/', views.student_new_message, name='student_new_message'),

    path('instructor_home/', views.instructor_home, name='instructor_home'),
    path('instructor_project_detail/', views.instructor_project_detail, name='instructor_project_detail'),
    path('instructor_new_project/', views.instructor_new_project, name='instructor_new_project'),
    path('instructor_add_project/', views.instructor_add_project, name='instructor_add_project'),
    path('instructor_project_change/', views.instructor_project_change, name='instructor_project_change'),    
    path('instructor_project_edit/', views.instructor_project_edit, name='instructor_project_edit'),  
    path('instructor_project_delete/', views.instructor_project_delete, name='instructor_project_delete'),
    path('instructor_project_remove/', views.instructor_project_remove, name='instructor_project_remove'),    
    path('logout/', views.logout, name='logout'),
    path('results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
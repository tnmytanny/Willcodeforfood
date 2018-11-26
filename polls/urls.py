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
    path('list/',views.list,name='list'),
    path('student_project_detail/', views.student_project_detail, name='student_project_detail'),
    path('student_project_apply/', views.student_project_apply, name='student_project_apply'),
    path('student_project_cancel/', views.student_project_cancel, name='student_project_cancel'),
    path('student_allocated_projects/', views.student_allocated_projects, name='student_allocated_projects'),
    path('student_project_accept/', views.student_project_accept, name='student_project_accept'),
    path('student_project_reject/', views.student_project_reject, name='student_project_reject'),
    path('student_edit_profile/', views.student_edit_profile, name='student_edit_profile'),
    path('student_profile/', views.student_profile, name='student_profile'),
    path('student_filter_project/', views.student_filter_project, name='student_filter_project'),
    path('search_chat/', views.search_chat, name='search_chat'),
    # path('student_inst_chat/', views.student_inst_chat, name='student_inst_chat'),
    # path('student_new_message/', views.student_new_message, name='student_new_message'),
    path('student_create_chat/', views.student_create_chat, name='student_create_chat'),
    path('student_show_messages/', views.student_show_messages, name='student_show_messages'),
    path('instructor_create_chat/', views.instructor_create_chat, name='instructor_create_chat'),
    path('instructor_show_messages/', views.instructor_show_messages, name='instructor_show_messages'),
    path('chat_detail/', views.chat_detail, name='chat_detail'),
    path('send_message/', views.send_message, name='send_message'),
    path('instructor_home/', views.instructor_home, name='instructor_home'),
    path('instructor_project_detail/', views.instructor_project_detail, name='instructor_project_detail'),
    path('instructor_new_project/', views.instructor_new_project, name='instructor_new_project'),
    path('instructor_project_create/', views.instructor_project_create, name='instructor_project_create'),
    path('instructor_project_change/', views.instructor_project_change, name='instructor_project_change'),
    path('change_password/', views.change_password, name='change_password'),
    path('instructor_project_edit/', views.instructor_project_edit, name='instructor_project_edit'),  
    path('instructor_project_delete/', views.instructor_project_delete, name='instructor_project_delete'),
    path('instructor_project_close/', views.instructor_project_close, name='instructor_project_close'),
    path('instructor_project_edit/', views.instructor_project_edit, name='instructor_project_edit'),
    path('instructor_allocated_projects/', views.instructor_allocated_projects, name='instructor_allocated_projects'),
    path('logout/', views.logout, name='logout'),
    path('results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
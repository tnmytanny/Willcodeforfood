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

    path('logout/', views.logout, name='logout'),
    path('results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
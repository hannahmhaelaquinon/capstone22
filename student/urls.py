from django.urls import path
from student import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('studentclick', views.studentclick_view),
    path('studentlogin', LoginView.as_view(
        template_name='student/studentlogin.html'), name='studentlogin'),
    path('studentsignup', views.student_signup_view, name='studentsignup'),
    path('student-dashboard', views.student_dashboard_view,
         name='student-dashboard'),
    path('student-exam', views.student_exam_view, name='student-exam'),
    path('take-exam/<int:pk>', views.take_exam_view, name='take-exam'),
    path('start-exam/<int:pk>', views.start_exam_view, name='start-exam'),

    path('calculate-marks', views.calculate_marks_view, name='calculate-marks'),
    path('view-result', views.view_result_view, name='view-result'),
    path('check-marks/<int:pk>', views.check_marks_view, name='check-marks'),
    path('student-marks', views.student_marks_view, name='student-marks'),
    path('student-video', views.student_video_view, name='student-video'),
    path('student-library', views.student_library_view, name='student-library'),
    path('student-games', views.student_games_view, name='student-games'),
    path('game/SimonSays', views.SimonGame, name='SimonSays'),
    path('student-calculate-bmi', views.studentbmi, name='student-bmi'),
    path('student-profile', views.studentprofile, name='student-profile'),
    # path('student-update/<int:pk>', views.student_update,
    #     name='student-update-profile'),




]

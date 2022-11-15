from django.urls import path
from teacher import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('teacherclick', views.teacherclick_view),
    path('teacherlogin', LoginView.as_view(
        template_name='teacher/teacherlogin.html'), name='teacherlogin'),
    path('teachersignup', views.teacher_signup_view, name='teachersignup'),
    path('teacher-dashboard', views.teacher_dashboard_view,
         name='teacher-dashboard'),
    path('teacher-video/', views.teacher_view_video, name='teacher-view-video'),
    path('teacher-add-video/', views.teacher_add_video, name='teacher-add-video'),
    path('game/SimonSays', views.SimonGame, name='SimonSays'),
    path('game/', views.tgame, name='game'),
    path('teacherlibrary/', views.tlibrary, name='library'),
    path('teacherprofile/', views.tprofile, name='profile'),
    path('profile-update/', views.teacherUpdate, name='teacher-update-profile'),


    path('teacher-assignment', views.teacher_assignment,
         name='teacher-assigbnment'),
    path('teacher-add-assignment', views.teacher_add_assignment,
         name='teacher-add-assignment'),
     path('teacher-edit-assignment', views.teacher_edit_assignment,
         name='teacher-edit-assignment'),

    path('teacher-exam', views.teacher_exam_view, name='teacher-exam'),
    path('teacher-add-exam', views.teacher_add_exam_view, name='teacher-add-exam'),
    path('teacher-view-exam', views.teacher_view_exam_view,
         name='teacher-view-exam'),
    path('delete-exam/<int:pk>', views.delete_exam_view, name='delete-exam'),


    path('teacher-question', views.teacher_question_view, name='teacher-question'),
    path('teacher-add-question', views.teacher_add_question_view,
         name='teacher-add-question'),
    path('teacher-view-question', views.teacher_view_question_view,
         name='teacher-view-question'),
    path('see-question/<int:pk>', views.see_question_view, name='see-question'),
    path('remove-question/<int:pk>',
         views.remove_question_view, name='remove-question'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

from django.urls import path, include
from django.contrib import admin
from admins import views
from django.contrib.auth.views import LogoutView, LoginView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('admin/', admin.site.urls),
    path('teacher/', include('teacher.urls')),
    path('student/', include('student.urls')),

    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup),

    # NAVBAR
    path('', views.home_view, name='home'),
    path('logout', LogoutView.as_view(
        template_name='admin/logout.html'), name='logout'),
    path('contactus', views.contactus_view, name='contactus'),
    path('afterlogin', views.afterlogin_view, name='afterlogin'),


    path('adminclick', views.adminclick_view, name='adminclick'),
    path('adminlogin', LoginView.as_view(
        template_name='admin/adminlogin.html'), name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view, name='admin-dashboard'),
    path('admin-teacher', views.admin_teacher_view, name='admin-teacher'),
    path('admin-view-teacher', views.admin_view_teacher_view,
         name='admin-view-teacher'),
    path('admin-add-teacher', views.admin_add_teacher_view,
         name='admin-add-teacher'),
    path('update-teacher/<int:pk>',
         views.update_teacher_view, name='update-teacher'),
    path('delete-teacher/<int:pk>',
         views.delete_teacher_view, name='delete-teacher'),
    path('admin-view-pending-teacher', views.admin_view_pending_teacher_view,
         name='admin-view-pending-teacher'),
    path('admin-view-teacher-salary', views.admin_view_teacher_salary_view,
         name='admin-view-teacher-salary'),
    path('approve-teacher/<int:pk>',
         views.approve_teacher_view, name='approve-teacher'),
    path('reject-teacher/<int:pk>',
         views.reject_teacher_view, name='reject-teacher'),

    path('admin-student', views.admin_student_view, name='admin-student'),
    path('admin-view-student', views.admin_view_student_view,
         name='admin-view-student'),
     path('admin-add-student', views.admin_add_student_view,
         name='admin-add-student'),
    path('admin-view-student-marks', views.admin_view_student_marks_view,
         name='admin-view-student-marks'),
    path('admin-view-marks/<int:pk>',
         views.admin_view_marks_view, name='admin-view-marks'),
    path('admin-check-marks/<int:pk>',
         views.admin_check_marks_view, name='admin-check-marks'),
    path('update-student/<int:pk>',
         views.update_student_view, name='update-student'),
    path('delete-student/<int:pk>',
         views.delete_student_view, name='delete-student'),

     path('admin-level', views.admin_level, name='admin-level'),
     path('admin-view-level', views.admin_view_levels, name='admin-view-level'),
     

     path('admin-section', views.admin_section_view, name='admin-section'),
     path('admin-add-level', views.admin_add_levels, name='admin-add-level'),
     path('delete-level/<int:pk>', views.admin_delete_levels, name='delete-level'),
     path('admin-add-section', views.admin_add_section, name='admin-add-section'),
     path('admin-view-section', views.admin_view_section, name='admin-view-section'),
     path('delete-section/<int:pk>',views.delete_section_view, name='delete-section'),

    path('admin-course', views.admin_course_view, name='admin-course'),
    path('admin-add-course', views.admin_add_course_view, name='admin-add-course'),
    path('admin-view-course', views.admin_view_course_view,
         name='admin-view-course'),
    path('delete-course/<int:pk>', views.delete_course_view, name='delete-course'),
    
    #subject
    path('admin-add-course', views.admin_add_course_view, name='admin-add-subject'),
    

    path('admin-question', views.admin_question_view, name='admin-question'),
    path('admin-add-question', views.admin_add_question_view,
         name='admin-add-question'),
    path('admin-view-question', views.admin_view_question_view,
         name='admin-view-question'),
    path('view-question/<int:pk>', views.view_question_view, name='view-question'),
    path('delete-question/<int:pk>',
         views.delete_question_view, name='delete-question'),

    path('admin-view-video/', views.admin_view_video, name='admin-view-video'),
    path('admin-add-video/', views.admin_add_video, name='admin-add-video'),
    path('admin-delete-video/<int:pk>/',
         views.admin_delete_video, name='admin-delete-video'),
    path('admin-update-video/<int:pk>/',
         views.admin_update_video, name='admin-update-video'),



    path('admin-view-library/', views.admin_view_library,
         name='admin-view-library'),
    path('admin-upload-book/', views.upload_book, name='admin-upload-book'),
    path('admin-delete-book/<int:pk>/',
         views.delete_book, name='admin-delete-book'),
    path('admin-edit-book/<int:pk>/', views.edit_book, name='admin-edit-book'),
    path('admin-update-file/<int:pk>/',
         views.admin_update_file, name='admin-update-file'),



    #path('admin-edit-library/', views.admin_edit_library.as_view(), name='admin-edit-library'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

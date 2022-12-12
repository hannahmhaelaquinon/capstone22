from django.shortcuts import render, redirect, reverse
from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from datetime import date, timedelta
from admins import models as QMODEL
from teacher import models as TMODEL
from teacher import forms as TFORM                              
from .forms import StudentForm, StudentUserForm, UpdateForm
from django.contrib import messages


# for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'student/studentclick.html')


def student_signup_view(request):
    userForm = forms.StudentUserForm()
    studentForm = forms.StudentForm()
    mydict = {'userForm': userForm, 'studentForm': studentForm}
    if request.method == 'POST':
        userForm = forms.StudentUserForm(request.POST)
        studentForm = forms.StudentForm(request.POST, request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            student = studentForm.save(commit=False)
            student.user = user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('studentlogin')
    return render(request, 'student/studentsignup.html', context=mydict)


def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    dict = {

        'total_course': QMODEL.Course.objects.all().count(),
        'total_question': QMODEL.Question.objects.all().count(),
        'total_assignment': TMODEL.TeacherAssignment.objects.all().count(),
    }
    return render(request, 'student/student_dashboard.html', {'context': dict, 'navbar': 'student-dashboard'})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_assignment(request):
    subject = QMODEL.Subject.objects.all()
    return render(request, 'student/student_assignment.html', {'subject': subject, 'navbar': 'student-assignment'})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_take_assignment(request, pk):
    subject = QMODEL.Subject.objects.get(id=pk)
    assignment = TMODEL.TeacherAssignment.objects.all().filter(subject=subject)
    if request.method == 'POST':
        pass
    response = render(request, 'student/student_take_assignment.html',
                      {'subject': subject, 'assignment': assignment})
    response.set_cookie('subject_id', subject.id)
    return response


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_exam_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request, 'student/student_exam.html', {'courses': courses, 'navbar': 'student-exam'})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def take_exam_view(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    total_questions = QMODEL.Question.objects.all().filter(course=course).count()
    questions = QMODEL.Question.objects.all().filter(course=course)
    total_marks = 0
    for q in questions:
        total_marks = total_marks + q.marks

    return render(request, 'student/take_exam.html', {'course': course, 'total_questions': total_questions, 'total_marks': total_marks})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def start_exam_view(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    questions = QMODEL.Question.objects.all().filter(course=course)
    if request.method == 'POST':
        pass
    response = render(request, 'student/start_exam.html',
                      {'course': course, 'questions': questions})
    response.set_cookie('course_id', course.id)
    return response


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def calculate_marks_view(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course = QMODEL.Course.objects.get(id=course_id)

        total_marks = 0
        questions = QMODEL.Question.objects.all().filter(course=course)
        for i in range(len(questions)):

            selected_ans = request.COOKIES.get(str(i+1))
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
        student = models.Student.objects.get(user_id=request.user.id)
        result = QMODEL.Result()
        result.marks = total_marks
        result.exam = course
        result.student = student
        result.save()

        return HttpResponseRedirect('view-result')


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def view_result_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request, 'student/view_result.html', {'courses': courses})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def check_marks_view(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    student = models.Student.objects.get(user_id=request.user.id)
    results = QMODEL.Result.objects.all().filter(
        exam=course).filter(student=student)
    return render(request, 'student/check_marks.html', {'results': results})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_marks_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request, 'student/student_marks.html', {'courses': courses})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_video_view(request):
    video = QMODEL.Video.objects.all()
    return render(request, 'student/svideo.html', {'video': video, 'navbar': 'student-video'})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_library_view(request):
    books = QMODEL.Library.objects.all()
    return render(request, 'student/slibrary.html', {'books': books, 'navbar': 'student-library'})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_games_view(request):
    return render(request, 'student/SGame/sgamehome.html', {'navbar': 'student-games'})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def SimonGame(request):
    return render(request, 'student/SGame/index.html')


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def studentbmi(request):
    return render(request, 'student/bmi.html')


@login_required(login_url='studetnlogin')
@user_passes_test(is_student)
def studentprofile(request):
    students = models.Student.objects.all()
    return render(request, 'student/sprofile.html',  {'students': students})


@login_required(login_url='studetnlogin')
@user_passes_test(is_student)
def studentupdate(request):
    if request.method == 'POST':
        user_form = UpdateForm(request.POST, instance=request.user)
        profile_form = StudentForm(
            request.POST, request.FILES, instance=request.user.student)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
           # messages.success(request, 'Your profile is updated successfully')
            return redirect('student-profile')

    else:
        user_form = UpdateForm(instance=request.user)
        profile_form = StudentForm(instance=request.user.student)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'student/update_student.html', context)

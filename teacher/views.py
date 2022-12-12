from django.shortcuts import render, redirect, reverse
from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from datetime import date, timedelta
from admins import models as QMODEL
from student import models as SMODEL
from admins import forms as QFORM
from teacher import forms as TFORM
from teacher import models as TMODEL
from django.contrib import messages
from .forms import TeacherForm, TeacherUserForm, UpdateTeacherForm

# for showing signup/login button for teacher


def teacherclick_view(request,):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'teacher/teacherclick.html')


def teacher_signup_view(request):
    userForm = forms.TeacherUserForm()
    teacherForm = forms.TeacherForm()
    mydict = {'userForm': userForm, 'teacherForm': teacherForm}
    if request.method == 'POST':
        userForm = forms.TeacherUserForm(request.POST)
        teacherForm = forms.TeacherForm(request.POST, request.FILES)
        if userForm.is_valid() and teacherForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            teacher = teacherForm.save(commit=False)
            teacher.user = user
            teacher.save()
            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
            return HttpResponseRedirect('teacherlogin')
    return render(request, 'teacher/teachersignup.html', context=mydict)


def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    sections = QMODEL.Section.objects.filter(teacher=request.user.teacher.id)
    section_id_list = []
    for section in sections:
        section = QMODEL.Section.objects.get(id=section.id)
        section_id_list.append(section.id)

    final_section = []
    # Removing Duplicate Course Id
    for id in section_id_list:
        if id not in final_section:
            final_section.append(id)

    students_count = SMODEL.Student.objects.filter(id__in=final_section).count()
    section_count = sections.count()
    level_count = sections.count()
    context = {
        "students_count": students_count,
        "section_id_list": section_id_list,
        "section_count": section_count
    }
    return render(request, 'teacher/teacher_dashboard.html', context)

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_subject(request):
    subjects = QMODEL.Subject.objects.all()
    return render(request, 'teacher/teacher_subject.html', {'subjects': subjects})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_subject(request):
    subjectForm = forms.SubjectForm()
    if request.method == 'POST':
        subjectForm = forms.SubjectForm(request.POST)
        if subjectForm.is_valid():
            subject = subjectForm.save(commit=False)
            subject.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-subject')
    return render(request, 'teacher/teacher_add_subject.html', {'subjectForm': subjectForm})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_exam_view(request):
    return render(request, 'teacher/teacher_exam.html')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_exam_view(request):
    courseForm = QFORM.CourseForm()
    if request.method == 'POST':
        courseForm = QFORM.CourseForm(request.POST)
        if courseForm.is_valid():
            courseForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-view-exam')
    return render(request, 'teacher/teacher_add_exam.html', {'courseForm': courseForm})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_assign_quiz(request):
    assignForm = forms.TeacherAssignForm()
    if request.method == 'POST':
        assignForm = forms.TeacherAssignForm(request.POST)
        if assignForm.is_valid():
            assign = assignForm.save(commit=False)
            course = QMODEL.Course.objects.get(id=request.POST.get('courseID'))
            subject = QMODEL.Subject.objects.get(
                id=request.POST.get('subjectID'))
            assign.course = course
            assign.subject = subject
            assign.save()
            assignForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-view-exam')
    return render(request, 'teacher/teacher_assign_quiz.html', {'assignForm': assignForm})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_answer(request):
    courses = QMODEL.Course.objects.all()
    questions = QMODEL.Question.objects.all()
    context = {
        'courses': courses,
        'questions': questions
    }
    return render(request, 'teacher/teacher_view_answer.html', context)


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_exam_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request, 'teacher/teacher_view_exam.html', {'courses': courses})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def delete_exam_view(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/teacher/teacher-view-exam')


@login_required(login_url='adminlogin')
def teacher_question_view(request):
    return render(request, 'teacher/teacher_question.html')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_question_view(request):
    questionForm = QFORM.QuestionForm()
    if request.method == 'POST':
        questionForm = QFORM.QuestionForm(request.POST)
        if questionForm.is_valid():
            question = questionForm.save(commit=False)
            course = QMODEL.Course.objects.get(id=request.POST.get('courseID'))
            question.course = course
            question.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-view-question')
    return render(request, 'teacher/teacher_add_question.html', {'questionForm': questionForm})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_assignment(request):
    courses = QMODEL.Course.objects.all()
    assignments = TMODEL.TeacherAssignment.objects.all()
    context = {
        'courses': courses,
        'assignments': assignments
    }
    return render(request, 'teacher/teacher_assignment.html', context)


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_assignment(request):
    assignmentForm = TFORM.TeacherAssForm()
    if request.method == 'POST':
        assignmentForm = TFORM.TeacherAssForm(request.POST, request.FILES)
        if assignmentForm.is_valid():
            assignment = assignmentForm.save(commit=False)
            subject = QMODEL.Subject.objects.get(id=request.POST.get('subjectID'))
            assignment.subject = subject
            assignment.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-assignment')
    return render(request, 'teacher/teacher_add_assignment.html', {'assignmentForm': assignmentForm})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_edit_assignment(request):
    ass_form = TFORM.TeacherAssForm(request.POST, request.FILES)
    context = {
        'ass_form': ass_form,
    }
    if request.method == 'POST':
        ass_form = TFORM.TeacherAssForm(request.POST, request.FILES)

        if ass_form.is_valid():
            assignment = ass_form.save()
            course = QMODEL.Course.objects.get(id=request.POST.get('courseID'))
            assignment.course = course
            assignment.save()
            return redirect('teacher-assignment')

    else:
        print("form is invalid")

    return render(request, 'teacher/teacher_edit_assignment.html', context)


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_video(request):
    videos = QMODEL.Video.objects.all()
    context = {
        'videos': videos
    }
    return render(request, 'teacher/teachervideo.html', context)


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_video(request):
    all_video = QMODEL.Video.objects.all()
    if request.method == "POST":
        form = QFORM.VideoForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('teacher-view-video')
    else:
        form = QFORM.VideoForm()
    return render(request, 'teacher/teacher_add_video.html', {"form": form, "all": all_video})


def teacher_delete_video(request, pk):
    if request.method == 'POST':
        video = QMODEL.Video.objects.get(pk=pk)
        video.delete()
    return redirect('teacher-view-video')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def SimonGame(request):
    return render(request, 'teacher/TGame/index.html')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def tgame(request):
    return render(request, 'teacher/TGame/tgamehome.html')


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def tlibrary(request):
    books = QMODEL.Library.objects.all()
    return render(request, 'teacher/teacherlibrary.html', {'books': books})


@login_required(login_url='teacherlogin')
def upload_book(request):
    if request.method == 'POST':
        form = QFORM.LibraryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('library')
    else:
        form = QFORM.LibraryForm()
    return render(request, 'teacher/teacher_upload_book.html', {'form': form})


'''
def delete_book(request, pk):
    if request.method == 'POST':
        book = QMODEL.Library.objects.get(pk=pk)
        book.delete()
    return redirect('library')
'''


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def tprofile(request):
    teacher = models.Teacher.objects.all()
    return render(request, 'teacher/teacherprofile.html',  {'teachers': teacher})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacherUpdate(request):
    if request.method == 'POST':
        user_form = UpdateTeacherForm(request.POST, instance=request.user)
        profile_form = TeacherForm(
            request.POST, request.FILES, instance=request.user.teacher)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
           # messages.success(request, 'Your profile is updated successfully')
            return redirect('profile')

    else:
        user_form = UpdateTeacherForm(instance=request.user)
        profile_form = TeacherForm(instance=request.user.teacher)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'teacher/update_teacher.html', context)


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_question_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request, 'teacher/teacher_view_question.html', {'courses': courses})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def see_question_view(request, pk):
    questions = QMODEL.Question.objects.all().filter(course_id=pk)
    return render(request, 'teacher/see_question.html', {'questions': questions})


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def remove_question_view(request, pk):
    question = QMODEL.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/teacher/teacher-view-question')

from django.shortcuts import get_object_or_404, render, redirect, reverse
from . import forms, models
from django.views.generic import View
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from teacher import models as TMODEL
from student import models as SMODEL
from teacher import forms as TFORM
from student import forms as SFORM
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from .forms import CourseForm, VideoForm, LibraryForm
from django.core.files.storage import FileSystemStorage


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'admin/index.html')


def signin(request):
    return render(request, 'signin.html')


def signup(request):
    return render(request, 'signup.html')


def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()


def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


def afterlogin_view(request):
    if is_student(request.user):
        return redirect('student/student-dashboard')

    elif is_teacher(request.user):
        accountapproval = TMODEL.Teacher.objects.all().filter(
            user_id=request.user.id, status=True)
        if accountapproval:
            return redirect('teacher/teacher-dashboard')
        else:
            return render(request, 'teacher/teacher_wait_for_approval.html')
    else:
        return redirect('admin-dashboard')

# Redirect to admin login page


def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')

# Shows admin dashboard with all teachers and pending teachers and students


@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    dict = {
        'total_student': SMODEL.Student.objects.all().count(),
        'total_teacher': TMODEL.Teacher.objects.all().filter(status=True).count(),
        'total_course': models.Course.objects.all().count(),
        'total_question': models.Question.objects.all().count(),
    }
    return render(request, 'admin/admin_dashboard.html', context=dict)

# Views all teacher created when clicked on the navbar


@login_required(login_url='adminlogin')
def admin_teacher_view(request):
    dict = {
        'total_teacher': TMODEL.Teacher.objects.all().filter(status=True).count(),
        'pending_teacher': TMODEL.Teacher.objects.all().filter(status=False).count(),
        'salary': TMODEL.Teacher.objects.all().filter(status=True).aggregate(Sum('salary'))['salary__sum'],
    }
    return render(request, 'admin/admin_teacher.html', context=dict)

# Single teacher vew


@login_required(login_url='adminlogin')
def admin_view_teacher_view(request):
    teachers = TMODEL.Teacher.objects.all().filter(status=True)
    return render(request, 'admin/admin_view_teacher.html', {'teachers': teachers})

#Register/Sign in teacher


@login_required(login_url='adminlogin')
def admin_add_teacher_view(request):
    userForm = TFORM.TeacherUserForm()
    teacherForm = TFORM.TeacherForm()
    mydict = {'userForm': userForm, 'teacherForm': teacherForm}
    if request.method == 'POST':
        userForm = TFORM.TeacherUserForm(request.POST)
        teacherForm = TFORM.TeacherForm(request.POST, request.FILES)
        if userForm.is_valid() and teacherForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            teacher = teacherForm.save(commit=False)
            teacher.user = user
            teacher.save()
            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
        return HttpResponseRedirect('admin-view-pending-teacher')
    return render(request, 'admin/admin_add_teacher.html', context=mydict)

#Register/Sign in student


@login_required(login_url='adminlogin')
def admin_add_student_view(request):
    userForm = SFORM.StudentUserForm()
    studentForm = SFORM.StudentForm()
    mydict = {'userForm': userForm, 'studentForm': studentForm}
    if request.method == 'POST':
        userForm = SFORM.StudentUserForm(request.POST)
        studentForm = SFORM.StudentForm(request.POST, request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            student = studentForm.save(commit=False)
            student.user = user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('admin-view-student')
    return render(request, 'admin/admin_add_student.html', context=mydict)

# Update teacher data


@login_required(login_url='adminlogin')
def update_teacher_view(request, pk):
    teacher = TMODEL.Teacher.objects.get(id=pk)
    user = TMODEL.User.objects.get(id=teacher.user_id)
    userForm = TFORM.TeacherUserForm(instance=user)
    teacherForm = TFORM.TeacherForm(request.FILES, instance=teacher)
    mydict = {'userForm': userForm, 'teacherForm': teacherForm}
    if request.method == 'POST':
        userForm = TFORM.TeacherUserForm(request.POST, instance=user)
        teacherForm = TFORM.TeacherForm(
            request.POST, request.FILES, instance=teacher)
        if userForm.is_valid() and teacherForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            teacherForm.save()
            return redirect('admin-view-teacher')
    return render(request, 'admin/update_teacher.html', context=mydict)

# Delete a teacher from the form


@login_required(login_url='adminlogin')
def delete_teacher_view(request, pk):
    teacher = TMODEL.Teacher.objects.get(id=pk)
    user = User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin-view-teacher')

# Views all pending teachers


@login_required(login_url='adminlogin')
def admin_view_pending_teacher_view(request):
    teachers = TMODEL.Teacher.objects.all().filter(status=False)
    return render(request, 'admin/admin_view_pending_teacher.html', {'teachers': teachers})


# Approves teacher and redirects to salary page
@login_required(login_url='adminlogin')
def approve_teacher_view(request, pk):
    teacherSalary = forms.TeacherSalaryForm()
    if request.method == 'POST':
        teacherSalary = forms.TeacherSalaryForm(request.POST)
        if teacherSalary.is_valid():
            teacher = TMODEL.Teacher.objects.get(id=pk)
            teacher.salary = teacherSalary.cleaned_data['salary']
            teacher.status = True
            teacher.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-pending-teacher')
    return render(request, 'admin/salary_form.html', {'teacherSalary': teacherSalary})

# Deletes the teachers pending request


@login_required(login_url='adminlogin')
def reject_teacher_view(request, pk):
    teacher = TMODEL.Teacher.objects.get(id=pk)
    user = User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin-view-pending-teacher')

# Views teacher salary


@login_required(login_url='adminlogin')
def admin_view_teacher_salary_view(request):
    teachers = TMODEL.Teacher.objects.all().filter(status=True)
    return render(request, 'admin/admin_view_teacher_salary.html', {'teachers': teachers})

# Views all student on admin view


@login_required(login_url='adminlogin')
def admin_student_view(request):
    dict = {
        'total_student': SMODEL.Student.objects.all().count(),
    }
    return render(request, 'admin/admin_student.html', context=dict)

# View Single student data


@login_required(login_url='adminlogin')
def admin_view_student_view(request):
    student = SMODEL.Student.objects.all()
    return render(request, 'admin/admin_view_student.html', {'student': student})

# Update Student data


@login_required(login_url='adminlogin')
def update_student_view(request, pk):
    student = SMODEL.Student.objects.get(id=pk)
    user = SMODEL.User.objects.get(id=student.user_id)
    userForm = SFORM.StudentUserForm(instance=user)
    studentForm = SFORM.StudentForm(request.FILES, instance=student)
    mydict = {'userForm': userForm, 'studentForm': studentForm}
    if request.method == 'POST':
        userForm = SFORM.StudentUserForm(request.POST, instance=user)
        studentForm = SFORM.StudentForm(
            request.POST, request.FILES, instance=student)
        if userForm.is_valid() and studentForm.is_valid():
            user = userForm.save()
            user.save()
            studentForm.save()
            return redirect('admin-view-student')
    return render(request, 'admin/update_student.html', context=mydict)

# Delete student data


@login_required(login_url='adminlogin')
def delete_student_view(request, pk):
    student = SMODEL.Student.objects.get(id=pk)
    user = User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return HttpResponseRedirect('/admin-view-student')


@login_required(login_url='adminlogin')
def admin_level(request):
    level = models.Levels.objects.all()
    context = {
        'level': level
    }
    return render(request, 'admin/admin_level.html', context)


@login_required(login_url='adminlogin')
def admin_view_section(request):
    sections = models.Section.objects.all()
    context = {
        'sections': sections
    }
    return render(request, 'admin/admin_view_section.html', context)

@login_required(login_url='adminlogin')
def delete_section_view(request, pk):
    section = models.Section.objects.get(id=pk)
    section.delete()
    return HttpResponseRedirect('/admin-grade1')

# aView all subjects created
@login_required(login_url='adminlogin')
def admin_section_view(request):
    section = models.Section.objects.all()
    context = {
        'section': section,
    }
    return render(request, 'admin/admin_sections.html', context)


@login_required(login_url='adminlogin')
def admin_add_levels(request):
    if request.method == 'POST':
        levForm = forms.LevelForm(request.POST)
        if levForm.is_valid():
            levForm.save()
            return redirect('admin-view-level')
    else:
        levForm = forms.LevelForm()
    context = {
        'levForm' : levForm
    }
    return render(request, 'admin/admin_add_level.html', context)

@login_required(login_url='adminlogin')
def admin_view_levels(request):
    level = models.Levels.objects.all()
    context = {
        'level': level,
    }
    return render(request, 'admin/admin_view_level.html', context)


@login_required(login_url='adminlogin')
def admin_delete_levels(request, pk):
    level = models.Levels.objects.get(id=pk)
    level.delete()
    return HttpResponseRedirect('/admin-view-level')

@login_required(login_url='adminlogin')
def admin_add_section(request):
    if request.method == 'POST':
        secForm = forms.SectionForm(request.POST)
        if secForm.is_valid():
            secForm.save()
            return redirect('admin-view-section')
    else:
        secForm = forms.SectionForm()
    context = {
        'secForm' : secForm
    }
    return render(request, 'admin/admin_add_sections.html', context)

# View all subjects created
@login_required(login_url='adminlogin')
def admin_course_view(request):
    total_subject = models.Course.objects.all().count()
    context = {
        'total_subject': total_subject,
    }
    return render(request, 'admin/admin_course.html', context)


# Add a new course
@login_required(login_url='adminlogin')
def admin_add_course_view(request):
    courseForm = forms.CourseForm()
    if request.method == 'POST':
        courseForm = forms.CourseForm(request.POST)
        if courseForm.is_valid():
            courseForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-course')
    return render(request, 'admin/admin_add_course.html', {'courseForm': courseForm})


# View a course
@login_required(login_url='adminlogin')
def admin_view_course_view(request):
    courses = models.Course.objects.all()
    return render(request, 'admin/admin_subjects.html', {'courses': courses})

# Delete course


@login_required(login_url='adminlogin')
def delete_course_view(request, pk):
    course = models.Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/admin-view-course')

# Edit Course data


@login_required(login_url='adminlogin')
def edit_course_view(request):
    if request.method == 'POST':
        subform = CourseForm(request.POST, instance=request.user)

        if subform.is_valid():
            subform.save()
           # messages.success(request, 'Your profile is updated successfully')
            return redirect('admin-view-course')
        else:
            subform = CourseForm(instance=request.user)

        return render(request, 'admin/cousre_update.html', {'subform': subform})

# View all available question


@login_required(login_url='adminlogin')
def admin_question_view(request):
    return render(request, 'admin/admin_question.html')

# Add a new question


@login_required(login_url='adminlogin')
def admin_add_question_view(request):
    questionForm = forms.QuestionForm()
    if request.method == 'POST':
        questionForm = forms.QuestionForm(request.POST)
        if questionForm.is_valid():
            question = questionForm.save(commit=False)
            course = models.Course.objects.get(id=request.POST.get('courseID'))
            question.course = course
            question.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-question')
    return render(request, 'admin/admin_add_question.html', {'questionForm': questionForm})

# View a specific question


@login_required(login_url='adminlogin')
def admin_view_question_view(request):
    courses = models.Course.objects.all()
    return render(request, 'admin/admin_view_question.html', {'courses': courses})

#


@login_required(login_url='adminlogin')
def view_question_view(request, pk):
    questions = models.Question.objects.all().filter(course_id=pk)
    return render(request, 'admin/view_question.html', {'questions': questions})


@login_required(login_url='adminlogin')
def delete_question_view(request, pk):
    question = models.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/admin-view-question')


@login_required(login_url='adminlogin')
def admin_view_student_marks_view(request):
    students = SMODEL.Student.objects.all()
    return render(request, 'admin/admin_view_student_marks.html', {'students': students})


@login_required(login_url='adminlogin')
def admin_view_marks_view(request, pk):
    courses = models.Course.objects.all()
    response = render(request, 'admin/admin_view_marks.html',
                      {'courses': courses})
    response.set_cookie('student_id', str(pk))
    return response


@login_required(login_url='adminlogin')
def admin_check_marks_view(request, pk):
    course = models.Course.objects.get(id=pk)
    student_id = request.COOKIES.get('student_id')
    student = SMODEL.Student.objects.get(id=student_id)

    results = models.Result.objects.all().filter(
        exam=course).filter(student=student)
    return render(request, 'admin/admin_check_marks.html', {'results': results})


def aboutus_view(request):
    return render(request, 'admin/aboutus.html')

# Contact


def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name = sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email), message, settings.EMAIL_HOST_USER,
                      settings.EMAIL_RECEIVING_USER, fail_silently=False)
            return render(request, 'admin/contactussuccess.html')
    return render(request, 'contactus.html', {'form': sub})

# Video


@login_required(login_url='adminlogin')
def admin_view_video(request):
    videos = models.Video.objects.all()
    context = {
        'videos': videos
    }
    return render(request, 'admin/admin_view_video.html', context)


@login_required(login_url='adminlogin')
def admin_add_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin-view-video')
    else:

        form = VideoForm()
    return render(request, 'admin/admin_add_video.html', {'form': form})


def admin_delete_video(request, pk):
    if request.method == 'POST':
        video = models.Video.objects.get(pk=pk)
        video.delete()
    return redirect('admin-view-video')

# trial


def admin_update_video(request, pk):
    if request.method == "POST":
        video = request.FILES['video']
        file_name = request.FILES['video'].name

        fs = FileSystemStorage()
        file = fs.save(video.name, video)
        fileurl = fs.url(file)
        report = file_name

        models.Library.objects.filter(id=pk).update(video=video)
        # messages.success(request,'File was uploaded succesfully!')
        return redirect('admin_add_video')
    else:
        return render(request, 'admin/admin_update_video.html')


# Library
@login_required(login_url='adminlogin')
def admin_view_library(request):
    books = models.Library.objects.all()
    return render(request, 'admin/admin_view_library.html', {'books': books})


@login_required(login_url='adminlogin')
def upload_book(request):
    if request.method == 'POST':
        form = LibraryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin-view-library')
    else:
        form = LibraryForm()
    return render(request, 'admin/admin_upload_book.html', {'form': form})


def post(self, request):
    if request.method == 'POST':
        if 'btnUpdate' in request.POST:
            print('update profile button clicked')
            pid = request.POST.get("pid")
            title = request.POST.get("title")
            subject = request.POST.get("subject")
            cover = request.POST.get("cover")
            pdf = request.POST.get("pdf")
            date = request.POST.get("date")
            print(date)
            # email = request.POST.get("student-email")
            # phone = request.POST.get("student-phone")
        # 	update_Booking = Booking.objects.filter(id = pid).update(book_name = book_name, book_date = book_date, book_no_children = book_no_children, book_no_adult = book_no_adult,
        # 	book_depart = book_depart, book_return = book_return)
        # 	print(update_Booking)
        # 	print('profile updated')
        # elif 'btnDelete' in request.POST:
        # 	print('delete button clicked')
        # pid = request.POST.get("bbooking-id")
        # pay = Booking.objects.filter(id = pid).delete()
        # print('Booking deleted')
        # return HttpResponse ('post')
        # return redirect('my_dashboard_view')


def delete_book(request, pk):
    if request.method == 'POST':
        book = models.Library.objects.get(pk=pk)
        book.delete()
    return redirect('admin-view-library')

# no use for now -- edit trial


@login_required(login_url='adminlogin')
def edit_book(request, pk):
    books = models.Library.objects.get(pk=pk)
    return render(request, 'admin/admin_edit_book.html', {'pk': pk, 'books': books})


def admin_update_file(request, pk):
    if request.method == "POST":
        pdf = request.FILES['pdf']
        file_name = request.FILES['pdf'].name

        fs = FileSystemStorage()
        file = fs.save(pdf.name, pdf)
        fileurl = fs.url(file)
        report = file_name

        models.Library.objects.filter(id=pk).update(pdf=pdf)
        # messages.success(request,'File was uploaded succesfully!')
        return redirect('admin-view-library')
    else:
        return render(request, 'admin/admin_update_book.html')

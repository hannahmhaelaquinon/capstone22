from django.shortcuts import render, redirect, reverse
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

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'exam/index.html')


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


def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    dict = {
        'total_student': SMODEL.Student.objects.all().count(),
        'total_teacher': TMODEL.Teacher.objects.all().filter(status=True).count(),
        'total_course': models.Course.objects.all().count(),
        'total_question': models.Question.objects.all().count(),
    }
    return render(request, 'exam/admin_dashboard.html', context=dict)


@login_required(login_url='adminlogin')
def admin_teacher_view(request):
    dict = {
        'total_teacher': TMODEL.Teacher.objects.all().filter(status=True).count(),
        'pending_teacher': TMODEL.Teacher.objects.all().filter(status=False).count(),
        'salary': TMODEL.Teacher.objects.all().filter(status=True).aggregate(Sum('salary'))['salary__sum'],
    }
    return render(request, 'exam/admin_teacher.html', context=dict)


@login_required(login_url='adminlogin')
def admin_view_teacher_view(request):
    teachers = TMODEL.Teacher.objects.all().filter(status=True)
    return render(request, 'exam/admin_view_teacher.html', {'teachers': teachers})


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
    return render(request, 'exam/update_teacher.html', context=mydict)


@login_required(login_url='adminlogin')
def delete_teacher_view(request, pk):
    teacher = TMODEL.Teacher.objects.get(id=pk)
    user = User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin-view-teacher')


@login_required(login_url='adminlogin')
def admin_view_pending_teacher_view(request):
    teachers = TMODEL.Teacher.objects.all().filter(status=False)
    return render(request, 'exam/admin_view_pending_teacher.html', {'teachers': teachers})


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
    return render(request, 'exam/salary_form.html', {'teacherSalary': teacherSalary})


@login_required(login_url='adminlogin')
def reject_teacher_view(request, pk):
    teacher = TMODEL.Teacher.objects.get(id=pk)
    user = User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin-view-pending-teacher')


@login_required(login_url='adminlogin')
def admin_view_teacher_salary_view(request):
    teachers = TMODEL.Teacher.objects.all().filter(status=True)
    return render(request, 'exam/admin_view_teacher_salary.html', {'teachers': teachers})


@login_required(login_url='adminlogin')
def admin_student_view(request):
    dict = {
        'total_student': SMODEL.Student.objects.all().count(),
    }
    return render(request, 'exam/admin_student.html', context=dict)


@login_required(login_url='adminlogin')
def admin_view_student_view(request):
    students = SMODEL.Student.objects.all()
    return render(request, 'exam/admin_view_student.html', {'students': students})


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
            user.set_password(user.password)
            user.save()
            studentForm.save()
            return redirect('admin-view-student')
    return render(request, 'exam/update_student.html', context=mydict)


@login_required(login_url='adminlogin')
def delete_student_view(request, pk):
    student = SMODEL.Student.objects.get(id=pk)
    user = User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return HttpResponseRedirect('/admin-view-student')


@login_required(login_url='adminlogin')
def admin_course_view(request):
    total_subject = models.Course.objects.all().count()
    context = {
        'total_subject': total_subject,
    }
    return render(request, 'exam/admin_course.html', context)


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
    return render(request, 'exam/admin_add_course.html', {'courseForm': courseForm})


@login_required(login_url='adminlogin')
def admin_view_course_view(request):
    courses = models.Course.objects.all()
    return render(request, 'exam/admin_view_course.html', {'courses': courses})


@login_required(login_url='adminlogin')
def delete_course_view(request, pk):
    course = models.Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/admin-view-course')


@login_required(login_url='adminlogin')
def admin_question_view(request):
    return render(request, 'exam/admin_question.html')


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
    return render(request, 'exam/admin_add_question.html', {'questionForm': questionForm})


@login_required(login_url='adminlogin')
def admin_view_question_view(request):
    courses = models.Course.objects.all()
    return render(request, 'exam/admin_view_question.html', {'courses': courses})


@login_required(login_url='adminlogin')
def view_question_view(request, pk):
    questions = models.Question.objects.all().filter(course_id=pk)
    return render(request, 'exam/view_question.html', {'questions': questions})


@login_required(login_url='adminlogin')
def delete_question_view(request, pk):
    question = models.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/admin-view-question')


@login_required(login_url='adminlogin')
def admin_view_student_marks_view(request):
    students = SMODEL.Student.objects.all()
    return render(request, 'exam/admin_view_student_marks.html', {'students': students})


@login_required(login_url='adminlogin')
def admin_view_marks_view(request, pk):
    courses = models.Course.objects.all()
    response = render(request, 'exam/admin_view_marks.html',
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
    return render(request, 'exam/admin_check_marks.html', {'results': results})


def aboutus_view(request):
    return render(request, 'exam/aboutus.html')


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
            return render(request, 'exam/contactussuccess.html')
    return render(request, 'contactus.html', {'form': sub})


@login_required(login_url='adminlogin')
def admin_view_video(request):
    videos = models.Video.objects.all()
    context = {
        'videos': videos
    }
    return render(request, 'exam/admin_view_video.html', context)

@login_required(login_url='adminlogin')
def admin_add_video(request):
    all_video = models.Video.objects.all()
    if request.method == "POST":
        form = forms.Video_form(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin-view-video')
    else:
        form = forms.Video_form()
    return render(request, 'exam/admin_add_video.html', {"form": form, "all": all_video})

# Library


class admin_view_library(View):
    @method_decorator(login_required(login_url='adminlogin'))
    def get(self, request):
        books = models.Library.objects.all()
        subject = models.Course.objects.all()
        context = {
            'books': books,
            'subjects': subject,
        }
        return render(request, 'exam/admin_view_library.html', context)

class admin_all_view_library(View):
    @method_decorator(login_required(login_url='adminlogin'))
    def get(self,request):
        book = models.Library1.objects.all()
        return render(request, 'exam/admin_view_library.html',{ "books" : book})

    def post(self,request):
                    if request.method == 'POST':	
                        if 'btnUpdate' in request.POST:	
                            print('update profile button clicked')
                            pid = request.POST.get("booking-id")			                          
                            Title = request.POST.get("Title")			
                            Subject = request.POST.get("Subject")
                            Date = request.POST.get("Date")
                            print(Date)
                            update_Booking = models.Library1.objects.filter(id = pid).update(Title = Title, Subject = Subject, Date = Date)
                            print(update_Booking)
                            print('profile updated')
                        elif 'btnDelete' in request.POST:
                            print('delete button clicked')
                        pid = request.POST.get("bbooking-id")
                        pay = models.Library1.objects.filter(id = pid).delete()
                        print('Booking deleted')
                        # return HttpResponse ('post')
                        return redirect('admin-view-library')

class admin_add_book(View):
    @method_decorator(login_required(login_url='adminlogin'))
    def get(self, request):
        return render(request, 'exam/admin_add_library.html')

    def post(self, request):		
        form = forms.LibraryForm(request.POST)	

        if form.is_valid():
            Title = request.POST.get("Title")
            Subject = request.POST.get("Subject")
            Date = request.POST.get("Date")

            form = models.Library1(Title = Title, Subject = Subject, Date = Date)
            form.save()
            #return HttpResponse('Student record saved!')			
            return redirect('admin-view-library')
            # except:
            # 	raise Http404
        else:
            print(form.errors)
            return HttpResponse('not valid')


@login_required(login_url='adminlogin')
class admin_add_library_view(View):
    def get(self, request):
        subname = models.Course.objects.all()
        subjects = models.Course.objects.all()
        book = models.Library.objects.all()
        context = {
            'book': book,
            'subjects': subname,
            'subjects': subjects,
        }
        return render(request, 'exam/admin_add_library.html', context)

    def post(self, request):
        form = forms.LibraryForm(request.POST)
        form = forms.LibraryForm(data=request.POST, files=request.FILES)
        file = request.POST.get("file")
        print(file)
        booktitle = request.POST.get("booktitle")
        print(booktitle)
        book_image = request.POST.get("book_image")
        print(book_image)
        subname = models.Course.objects.get(
            title=request.POST.get("subjects", None))
        print(subname)

        if form.is_valid():
            booktitle = request.POST.get("booktitle")
            book_image = request.POST.get("book_image")
            subname = models.Course.objects.get(
                title=request.POST.get("subname"))
            file = request.POST.get("file")

        form = models.Library(booktitle=booktitle, subject=subname,
                       book_image=book_image)

        form.save()

        # return render(request, 'admin/add-subjects.html')
        return redirect('admin-view-library')

class admin_edit_library(View):
    @method_decorator(login_required(login_url='adminlogin'))
    def get(self, request):
        return render(request, 'exam/admin_edit_library.html')
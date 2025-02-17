from django.shortcuts import render
from django.contrib import messages
from .models import Students, Attendances,Subjects,Courses,Staff

# Student Views
def index(request):
    """Display list of all students."""
    data = Students.objects.all()
    context = {"data": data}
    return render(request, 'index.html', context)

def insertData(request):
    """Insert new student record."""
    if request.method == "POST":
        id = request.POST.get('id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        course=request.POST.get('course')
        
        query = Students(
            id=id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            gender=gender,
            course=course
        )
        query.save()
        messages.info(request, "Data inserted successfully")
        
        data = Students.objects.all()
        context = {"data": data}
        return render(request, 'index.html', context)
    return render(request, 'index.html')

def updateData(request, id):
    """Update existing student record."""
    if request.method == "POST":
        student = Students.objects.get(id=id)
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.email = request.POST.get('email')
        student.password = request.POST.get('password')
        student.gender = request.POST.get('gender')
        student.course = request.POST.get('course')
        student.save()
        
        messages.warning(request, "Data updated successfully")
        data = Students.objects.all()
        context = {"data": data}
        return render(request, 'index.html', context)
    
    d = Students.objects.get(id=id)
    context = {"d": d}
    return render(request, 'edit.html', context)

def deleteData(request,id):
    """Delete student record."""
    student = Students.objects.get(id=id)
    student.delete()
    messages.error(request, "Data deleted successfully")
    
    data = Students.objects.all()
    context = {"data": data}
    return render(request, 'index.html', context)

# Attendance Views
def attendance(request):
    """Display list of all attendance records."""
    attendance_list = Attendances.objects.all()
    context = {"attendance_list": attendance_list}
    return render(request, 'attendance.html',context)

def subject(request):
    """Display list of all subject records."""
    subject_list = Subjects.objects.all()
    context = {"subject_list": subject_list}
    return render(request, 'subject.html',context)

def AddSubject(request):
    if request.method == "POST":
        id=request.POST.get('id')
        course=request.POST.get('course')
        subject_name=request.POST.get('subject_name')
        staff=request.POST.get('staff')

        print(id)
        print(course)
        print(subject_name)
        print(staff)


        query=Subjects(
            id=id,
            course=course,
            subject_name=subject_name,
            staff=staff
        )
        query.save()
        messages.info(request,"Subject added successfully")

        subject_list = Subjects.objects.all()
        context= {"subject_list":subject_list}
        return render(request,'subject.html',context)
    return render(request, 'subject.html')


def insert_attendance(request):
    """Insert new attendance record."""
    if request.method == "POST":
        id = request.POST.get('id')
        subject = request.POST.get('subject')
        status = request.POST.get('status')
        
        query = Attendances(
             id=id,
             subject=subject,
             status=status
        )
        query.save()
        messages.info(request, "Attendance recorded successfully")
        
        attendance_list = Attendances.objects.all()
        context = {"attendance_list": attendance_list}
        return render(request, 'attendance.html', context)
    
    attendance_list = Attendances.objects.all()
    context = {"attendance_list": attendance_list}
    return render(request, 'attendance.html', context)

# Other Views
def about(request):
    """Display about page."""
    return render(request, 'about.html')

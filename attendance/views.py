from django.shortcuts import render , redirect, get_object_or_404
from django.contrib import messages
from .models import User, Students, Attendances,Subjects,Courses,Staff
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login,logout as auth_logout



from rest_framework import viewsets

from .models import Students
from .serializers import StudentSerializer
from .serializers import StaffSerializer
from .serializers import CourseSerializer


def admin_required(view_func):
    @login_required
    def wrapped(request, *args, **kwargs):
        if not request.is_admin:
            messages.error(request, "You don't have permission to perform this action.")
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return wrapped

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Set session variable for easy access in templates
            request.session['is_admin'] = user.is_admin()
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            # In a real-world scenario, passwords should be hashed
            if user.password == password:
                # Set session variables
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                request.session['is_admin'] = (user.role == 'admin')
                
                messages.success(request, f"Welcome back, {user.name}!")
                return redirect('index')
            else:
                messages.error(request, "Invalid password")
        except User.DoesNotExist:
            messages.error(request, "Email not found")
    
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'register.html')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use")
            return render(request, 'register.html')
        
        # Create new user
        user = User(
            name=name,
            email=email,
            password=password,  # In a real app, use password hashing
            role='user'  # Default role is user
        )
        user.save()
        
        messages.success(request, "Registration successful! Please login.")
        return redirect('login')
    
    return render(request, 'register.html')

def logout(request):
    # Clear session
    request.session.flush()
    messages.info(request, "You have been logged out.")
    return redirect('login')

# Student Views
def index(request):
    """Display list of all students."""
    data = Students.objects.all()
    context = {"data": data}
    return render(request, 'index.html', context)

@admin_required
def insertData(request):
    """Insert new student record."""
    if request.method == "POST":
        id = request.POST.get('id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        program=request.POST.get('program')
        
        query = Students(
            id=id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            gender=gender,
            program=program
        )

        if id and Students.objects.filter(id=id).exists():
            messages.error(request, "Student ID already exists")
            return redirect('index')
        
        query.save()
        messages.info(request, "Data inserted successfully")
        
        data = Students.objects.all()
        context = {"data": data}
        return render(request, 'index.html', context)
    return render(request, 'index.html')
pass

@admin_required
def updateData(request, id):
    """Update existing student record."""
    if request.method == "POST":
        student = Students.objects.get(id=id)
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.email = request.POST.get('email')
        student.gender = request.POST.get('gender')
        student.program = request.POST.get('program')
        student.save()
        
        messages.warning(request, "Data updated successfully")
        data = Students.objects.all()
        context = {"data": data}
        return render(request, 'index.html', context)
    
    d = Students.objects.get(id=id)
    context = {"d": d}
    return render(request, 'edit.html', context)
pass

@admin_required
def deleteData(request,id):
    """Delete student record."""
    student = Students.objects.get(id=id)
    student.delete()
    messages.error(request, "Data deleted successfully")
    
    data = Students.objects.all()
    context = {"data": data}
    return render(request, 'index.html', context)
pass

# Attendance Views

@admin_required
def add_attendance(request):
    if request.method == "POST":
        id = request.POST.get('id')
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject_name')
        status = request.POST.get('status')
        
        try:
            # Verify the subject exists
            subject = Subjects.objects.get(id=subject_id)
            
            new_attendance = Attendances(
                id=id,
                subject_id=subject, 
                subject_name=subject_name,
                status=status,
            )
            new_attendance.save()
            messages.success(request, "Attendance recorded successfully")
        except Subjects.DoesNotExist:
            messages.error(request, f"Subject with ID {subject_id} does not exist")
        
        return redirect('attendance')
    
    # Get all subjects for the dropdown
    subjects = Subjects.objects.all()
    attendance_list = Attendances.objects.all()
    context = {
        "attendance_list": attendance_list,
        "subjects": subjects
    }
    return render(request, 'attendance.html', context)
pass





@admin_required
def update_attendance(request, id):
    attendance_record = get_object_or_404(Attendances, id=id)
    
    if request.method == "POST":
        try:
            # Get the subject ID from the form
            subject_id_value = request.POST.get('subject_id')
            
            # Get the actual Subject object
            subject_obj = Subjects.objects.get(id=subject_id_value)
            
            # Update the attendance record
            attendance_record.subject_id = subject_obj
            attendance_record.subject_name = request.POST.get('subject_name')
            attendance_record.status = request.POST.get('status')
            attendance_record.save()
            
            messages.success(request, "Attendance updated successfully")
            return redirect('attendance')
        except Subjects.DoesNotExist:
            messages.error(request, f"Subject with ID {request.POST.get('subject_id')} does not exist")
    
    # Get all subjects for the dropdown
    subjects = Subjects.objects.all()
    context = {
        "attendance": attendance_record,
        "subjects": subjects  
    }
   
    return render(request, 'edit_attendance.html', context)
pass

@admin_required
def delete_attendance(request, id):
 attendance = get_object_or_404(Attendances, id=id)
 attendance.delete()
 messages.success(request, "Attendance record deleted successfully")
 return redirect('attendance')
pass


def subject(request):
    """Display list of all subject records."""
    subject_list = Subjects.objects.all()
    context = {"subject_list": subject_list}
    return render(request, 'subject.html', context)


@admin_required
def AddSubject(request):
    if request.method == "POST":
        # Collect form data
        course_id = request.POST.get('course_id')
        course_name = request.POST.get('course_name')
        subject_name = request.POST.get('subject_name')
        staff = request.POST.get('staff')
        
        # For debugging/logging purposes
        print( course_id, course_name, subject_name, staff)
        
        try:
            staff_instance = Staff.objects.filter(full_name=staff).first()
            
            course_instance = Courses.objects.get(course_id=course_id)
            
        
            if id and Subjects.objects.filter(id=course_id).exists():
                messages.error(request, "Subject ID already exists")
                return redirect('subject')
            
            # Create new subject record
            new_subject = Subjects(
                id=course_id,
                course_id=course_instance,  # Pass the course object, not the ID string
                course_name=course_name,
                subject_name=subject_name,
                staff=staff_instance
            )
            new_subject.save()
            messages.info(request, "Subject added successfully")
            return redirect('subject')
            
        except Staff.DoesNotExist:
            messages.error(request, f"Staff with name '{staff}' does not exist")
            return redirect('subject')
        except Courses.DoesNotExist:
            messages.error(request, f"Course with ID '{course_id}' does not exist")
            return redirect('subject')
            
    return render(request, 'subject.html')
pass

@admin_required
def EditSubject(request, subject_id):
    # Get the subject instance or return 404 if not found
    subject_instance = get_object_or_404(Subjects, id=subject_id)
    
    if request.method == "POST":
        # Update fields based on form data
        subject_instance.course_id = request.POST.get('course_id')
        subject_instance.course_name = request.POST.get('course_name')
        subject_instance.subject_name = request.POST.get('subject_name')
        
        staff = request.POST.get('staff')
        subject_instance.staff = Staff.objects.get(full_name=staff)
        
        subject_instance.save()
        messages.success(request, "Subject updated successfully")
        return redirect('subject')
    
    # Pass the current subject instance to the template
    context = {"subject": subject_instance}
    return render(request, 'edit_subject.html', context)
pass

@admin_required
def DeleteSubject(request, subject_id):
    subject_instance = get_object_or_404(Subjects, id=subject_id)
    
    if request.method == "POST":
        subject_instance.delete()
        messages.success(request, "Subject deleted successfully")
        return redirect('subject')
    
    # Render a confirmation page
    context = {"subject": subject_instance}
    return render(request, 'delete_subject.html', context)
pass

def course_list(request):
    """Display course page with all courses."""
    course_member = Courses.objects.all()
    context = {"course_member": course_member}
    return render(request, 'course.html', context)
@admin_required
def add_course(request):
    """Add a new course."""
    if request.method == "POST":
        course_id = request.POST.get('id')  
        course_name = request.POST.get('course_name')
        
        # Input validation
        if course_id and Courses.objects.filter(course_id=course_id).exists():
            messages.error(request, "Course ID already exists")
            return redirect('course')
        
        
            
        # Create new course object
        new_course = Courses(
            course_name=course_name,
        )
        
        if course_id:
            new_course.course_id = course_id
            
        new_course.save()
        messages.success(request, "Course added successfully")
        return redirect('course')
    
    # This handles the GET request if needed
    course_member = Courses.objects.all()
    context = {"course_member": course_member}
    return render(request, 'course.html', context)
pass

@admin_required
def update_course(request, course_id):
    """Update existing course record."""
    course_member = get_object_or_404(Courses, course_id=course_id)
    
    if request.method == "POST":
        course_name = request.POST.get('course_name')
        
        # Update course data
        course_member.course_name = course_name
        course_member.save()
        
        messages.success(request, "Course updated successfully")
        return redirect('course/')
    
    context = {"course": course_member}
    return render(request, 'edit_course.html', context)
pass

@admin_required
def delete_course(request, course_id):
    """Delete existing course record."""
    course_member = get_object_or_404(Courses, course_id=course_id)
    course_member.delete()
    messages.success(request, "Course deleted successfully")
    return redirect('course')
pass

def staff(request):
    """Display staff page with list of all staff members."""
    staff_list = Staff.objects.all()
    context = {"staff_list": staff_list}
    return render(request, 'staff.html', context)

@admin_required
def add_staff(request):
    """Add a new staff member."""
    if request.method == "POST":
        id = request.POST.get('id')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')

        if id and Staff.objects.filter(id=id).exists():
            messages.error(request, "Staff ID already exists")
            return redirect('staff')
        

        
        # Create new staff object
        new_staff = Staff(
            id=id if id else None,
            full_name=full_name,
            email=email
        )

        
        new_staff.save()
        messages.success(request, "Staff added successfully")
        return redirect('staff')
    
    return render(request, 'staff.html')
pass

@admin_required
def update_staff(request, staff_id):
    """Update an existing staff member."""
    staff_member = get_object_or_404(Staff, id=staff_id)
    
    if request.method == "POST":
        staff_member.full_name = request.POST.get('full_name')
        staff_member.email = request.POST.get('email')
        staff_member.save()
        messages.success(request, "Staff updated successfully")
        return redirect('staff')
    
    context = {"staff": staff_member}
    return render(request, 'update_staff.html', context)
pass

@admin_required
def delete_staff(request, staff_id):
    """Delete a staff member."""
    staff_member = get_object_or_404(Staff, id=staff_id)
    staff_member.delete()
    messages.success(request, "Staff deleted successfully")
    return redirect('staff')
pass



# Other Views
def about(request):
    """Display about page."""
    return render(request, 'about.html')




class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer

    def get_queryset(self):
        return Students.objects.all()

    def perform_create(self, serializer):
        serializer.save(id=self.request.id)

class StaffViewSet(viewsets.ModelViewSet):
    serializer_class = StaffSerializer

    def get_queryset(self):
        return Staff.objects.all()

    def perform_create(self, serializer):
        serializer.save(id=self.request.id)

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

    def get_queryset(self):
        return Courses.objects.all()

    def perform_create(self, serializer):
        serializer.save(id=self.request.id)

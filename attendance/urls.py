# from django.urls import path
from attendance import views

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet
from .views import StaffViewSet
from .views import CourseViewSet

urlpatterns = [
    # Main pages
    path('', views.index, name="index"),
    # path('attendance', views.attendance, name="attendance"),
    path("subject", views.subject, name="subject"),
    
    path('staff', views.staff, name='staff'),
    path('add_staff/', views.add_staff, name='add_staff'),
    path('update/<int:staff_id>/', views.update_staff, name='update_staff'),
    path('delete/<int:staff_id>/', views.delete_staff, name='delete_staff'),

    path('attendance', views.add_attendance, name="attendance"),
    path('update/<int:id>/', views.update_attendance, name='update_attendance'),
    path('delete/<int:id>/', views.delete_attendance, name='delete_attendance'),

    path('course/', views.course_list, name="course"),
    path('add_course/', views.add_course, name="add_course"),
    path('update_course/<int:course_id>/', views.update_course, name='update_course'),
    path('delete_course/<int:course_id>/', views.delete_course, name='delete_course'),
    #  data operations
    path('insert', views.insertData, name="insertData"),
    path('update/<id>', views.updateData, name="updateData"),
    path('delete/<id>', views.deleteData, name="deleteData"),
    
    # path('attendances', views.insert_attendance, name="attendances"),
    path('subject/', views.subject, name='subject'),
    path('subject/add', views.AddSubject, name='add_subject'),
    path('subject/edit/<int:subject_id>/', views.EditSubject, name='edit_subject'),
    path('subject/delete/<int:subject_id>/', views.DeleteSubject, name='delete_subject'),
    
   
]
   



router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='languages')
router.register(r'staff', StaffViewSet, basename='language')
router.register(r'course', CourseViewSet, basename='lang')


urlpatterns = [
    path('api/', include(router.urls)),
    

     # Main pages
    path('', views.index, name="index"),
    path("subject", views.subject, name="subject"),
    
    path('staff', views.staff, name='staff'),
    path('add_staff/', views.add_staff, name='add_staff'),
    path('update/<int:staff_id>/', views.update_staff, name='update_staff'),
    path('delete/<int:staff_id>/', views.delete_staff, name='delete_staff'),

    path('course/', views.course_list, name="course"),
    path('add_course/', views.add_course, name="add_course"),
    path('update_course/<int:course_id>/', views.update_course, name='update_course'),
    path('delete_course/<int:course_id>/', views.delete_course, name='delete_course'),
    #  data operations
    path('insert', views.insertData, name="insertData"),
    path('update/<id>', views.updateData, name="updateData"),
    path('delete/<id>', views.deleteData, name="deleteData"),
    
    path('attendance', views.add_attendance, name="attendance"),
    path('update/<int:id>/', views.update_attendance, name='update_attendance'),
    path('delete/<int:id>/', views.delete_attendance, name='delete_attendance'),

    path('subject/', views.subject, name='subject'),
    path('subject/add', views.AddSubject, name='add_subject'),
    path('subject/edit/<int:subject_id>/', views.EditSubject, name='edit_subject'),
    path('subject/delete/<int:subject_id>/', views.DeleteSubject, name='delete_subject'),
    
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    

    
]

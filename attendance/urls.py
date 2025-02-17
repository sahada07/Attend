from django.urls import path
from attendance import views

urlpatterns = [
    # Main pages
    path('', views.index, name="index"),
    path('attendance', views.attendance, name="attendance"),
    path("subject", views.subject, name="subject"),

    # Student data operations
    path('insert', views.insertData, name="insertData"),
    path('update/<id>', views.updateData, name="updateData"),
    path('delete/<id>', views.deleteData, name="deleteData"),
    path('attendances', views.insert_attendance, name="attendances"),
    path('subject/add', views.AddSubject, name="add_subject"),
]
   
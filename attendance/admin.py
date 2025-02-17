from django.contrib import admin
from .models import Admin, Staff, Courses, Subjects, Students, Attendances, AttendanceReport, LeaveReportStudent, LeaveReportStaff, FeedbackStudent, FeedbackStaff, NotificationStudent, NotificationStaff

admin.site.register(Admin)
admin.site.register(Staff)
admin.site.register(Courses)
admin.site.register(Subjects)
admin.site.register(Students)
admin.site.register(Attendances)
admin.site.register(AttendanceReport)
admin.site.register(LeaveReportStudent)
admin.site.register(LeaveReportStaff)
admin.site.register(FeedbackStudent)
admin.site.register(FeedbackStaff)
admin.site.register(NotificationStudent)
admin.site.register(NotificationStaff)



# Create a new file middleware.py in your app directory
from django.shortcuts import redirect
from django.contrib import messages

class RoleBasedAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before the view is called
        if request.user.is_authenticated:
            # Store the user role in the request for easy access in views
            request.is_admin = request.user.is_admin() if hasattr(request.user, 'is_admin') else False
        
        response = self.get_response(request)
        return response
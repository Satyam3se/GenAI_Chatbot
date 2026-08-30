from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

def dashboard_view(request):
    # Restrict dashboard to HR users only
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to access the Dashboard.")
        return redirect('main:login')
    
    if hasattr(request.user, 'profile') and request.user.profile.role != 'hr':
        messages.error(request, "Access Denied. The Dashboard is for HR Managers only.")
        return redirect('chat_app:chat_interface')
    
    return render(request, 'dashboard/lead_dashboard.html', {'leads': []})
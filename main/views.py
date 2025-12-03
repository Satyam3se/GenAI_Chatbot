from django.shortcuts import render, redirect
from django.http import HttpResponse

def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Lead data is no longer saved to Firestore.
        # You can add other lead processing logic here if needed.
        
        # Redirect to a thank you page or back to the home page
        return redirect('main:thank_you')
    
    return render(request, 'main/index.html')

def thank_you(request):
    return render(request, 'main/thank_you.html')
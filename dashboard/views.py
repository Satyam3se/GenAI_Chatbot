from django.shortcuts import render
from django.http import HttpResponse

def dashboard_view(request):
    # Leads are no longer fetched from Firestore.
    # You can add other dashboard data processing logic here if needed.
    return render(request, 'dashboard/lead_dashboard.html', {'leads': []})
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.template import loader
# Create your views here.
from django.shortcuts import render
from .models import *




# Create your views here.
def home(request):
    return render (request, './dashboard/index.html')

def about(request):
    return render (request, './dashboard/about.html')

def services(request):
    return render (request, './dashboard/services.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message_text = request.POST.get('message', '').strip()

        # Basic validation
        if name and email and subject and message_text:
            # Save to database
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message_text
            )
            messages.success(request, 'Your message has been sent. Thank you!')
        else:
            messages.error(request, 'Please fill all the fields.')

        # Convert messages to list for template if you want latest message only
        msgs = list(messages.get_messages(request))

        return render(request, 'dashboard/contact.html', {'messages_list': msgs})

    return render(request, 'dashboard/contact.html')
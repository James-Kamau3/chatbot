from django.shortcuts import render, redirect
from dotenv import load_dotenv
from django.contrib.auth.models import User
from django.http import JsonResponse
import os
from django.contrib import auth
from .models import Chat
from django.utils import timezone
import google.generativeai as genai



# Create your views here.

load_dotenv()
genai.configure(api_key=os.environ["API_KEY"])

def gemni(message):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(message)
        return response.text

    except Exception as e:
        return f"An error occurred: {str(e)}"

def chatApp(request):
 
    if request.method == 'POST':
        message = request.POST.get('message')
        response = gemni(message)
        if request.user.is_authenticated:
            chat = Chat(user = request.user, message=message, response=response, created_at= timezone.now())
            chat.save()
        return JsonResponse({'message': message, 'response': response})

    return render(request, 'chatbot.html')



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatApp')
        else:
            error_message = 'Invalid credentials'
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('chatApp')
            except Exception as e:
                error_message = f'Error creating account: {e}'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Password dont match'
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')



def logout(request):
    auth.logout(request)
    return redirect('login')

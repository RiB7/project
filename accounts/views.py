from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model  # gets the user_model django  default or your own custom
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
# Create your views here.
from .models import *
from .forms import  CreateUserForm
from django.contrib.auth.models import User

def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)

				return redirect('login')
			

		context = {'form':form}
		return render(request, 'accounts/register.html', context)




def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST['username']
			password = request.POST['password']
			if '@' in username:
				username = User.objects.get(email=username).username
				user = auth.authenticate(username=username, password=password)
			else:
				user = auth.authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					auth.login(request, user)
					# Redirect to index page.
					return redirect("home")
				else:
					context = {}
					return render(request, 'accounts/login.html', context)
			else:
				context = {}
				return render(request, 'accounts/login.html', context)
		# if request.method == 'POST':
		# 	username = request.POST.get('username')
		# 	password =request.POST.get('password')
		#
		# 	user = authenticate(request, username=username, password=password)
		#
			# if user is not None:
			# 	login(request, user)
			# 	return redirect('home')
			# else:
			# 	messages.info(request, 'Username OR password is incorrect')
		else:
			context = {}
			return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')


@login_required(login_url='login')
def home(request):
	return render(request, 'accounts/dashboard.html')





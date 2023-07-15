from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import UserRegistrationForm
from main.models import Teacher


def user_login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Avval akkauntdan chiqib oling')
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            user = None

        if user:
            user = authenticate(request, username=user.username, password=password)

        if user:
            login(request, user)
            messages.success(request, f'Xush kelibsiz, {user.first_name} {user.last_name}')
            return redirect('home')
        else:
            messages.error(request, 'E-mail yoki Parol xato')
            return redirect('login')

    context = {
        "auth": True
    }
    return render(request, "users/login.html", context)


def user_register(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Avval akkauntdan chiqib oling')
        return redirect('home')

    if request.method == 'POST':
        try:
            user = User.objects.get(email=request.POST.get('email'))
        except:
            user = None

        print(request.POST)
        if user:
            messages.info(request, 'Bunday foydalanuvchu allaqachon mavjud')
            return redirect('register')

        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akkaunt muvaffaqiyatli ochildi')
            return redirect('login')
        else:
            messages.error(request, "Forma noto'g'ri to'ldirildi")
            return redirect('register')

    # form = UserRegistrationForm()
    context = {
        "auth": True,
        # "form": form,
    }
    return render(request, "users/register.html", context)


def user_logout(request):
    messages.info(request, "Tizimdan chiqdingiz")
    logout(request)
    return redirect('login')

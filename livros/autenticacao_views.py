# livros/autenticacao_views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Perfil


# 1. REGISTRO (CRIAR CONTA)
def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Conta criada com sucesso!")
            return redirect('livros:home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'autenticacao/registro.html', {'form': form})


# 2. LOGIN
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.info(request, f"Bem-vindo(a), {user.first_name}!")
            return redirect('livros:home')
        else:
            messages.error(request, "E-mail ou senha inválidos.")

    form = AuthenticationForm()
    return render(request, 'autenticacao/login.html', {'form': form})


# 3. LOGOUT
def logout_view(request):
    logout(request)
    messages.info(request, "Você saiu da sua conta.")
    return redirect('livros:login_view')

@login_required
def perfil(request):
    perfil, created = Perfil.objects.get_or_create(user=request.user)
    return render(request, 'livros/perfil.html', {'perfil': perfil})

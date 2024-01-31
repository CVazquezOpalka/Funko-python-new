from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from store.forms import CustomUserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from store.models import User, Profile, Oreden_de_pago


def registrar(request):
    form = CustomUserForm()
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario creado satisfactoriamente")
            return redirect("iniciarsesion")
    context = {"form": form}
    return render(request, "auth/registrar.html", context)


def iniciar_sesion(request):
    if request.user.is_authenticated:
        messages.warning(request, "El usuario ya inicio sesión")
        return redirect("home")
    else:
        if request.method == "POST":
            name = request.POST.get("username")
            contraseña = request.POST.get("password")
            user = authenticate(request, username=name, password=contraseña)
            if user is not None:
                login(request, user)
                messages.success(request, "Has iniciado sesión correctamente")
                return redirect("home")
            else:
                context = {"error": "Nombre de usuario o contraseña invalidos"}
                return render(request, "auth/signin.html", context)
        else:
            return render(request, "auth/signin.html")


def cerrar_sesion(request):
    logout(request)
    messages.success(request, "Has cerrado sesión")
    return redirect("home")


@login_required
def mi_cuenta(request):
    user = User.objects.get(id=request.user.id)
    perfil = Profile.objects.filter(user=request.user).first()
    orden = Oreden_de_pago.objects.filter(user=request.user)
    context = {"perfil": perfil, "user": user, "orden":orden}
    return render(request, "auth/micuenta.html", context)

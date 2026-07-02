from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from .forms import LoginForm, UpdatePasswordForm, UserRegisterForm
from .models import User


class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('app_users:login')

    def form_valid(self, form):
        User.objects.create_user(
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            occupation=form.cleaned_data['occupation'],
            gender=form.cleaned_data['gender'],
            date_birth=form.cleaned_data['date_birth'],
            phone=form.cleaned_data.get('phone', ''),
        )
        return super().form_valid(form)


class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('app_users:dashboard')

    def form_valid(self, form):
        user = authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )
        if user is None:
            form.add_error(None, 'Email o contraseña incorrectos.')
            return self.form_invalid(form)
        login(self.request, user)
        return super().form_valid(form)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('app_users:login'))


class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name = 'users/cambiar_password.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('app_users:login')
    login_url = reverse_lazy('app_users:login')

    def form_valid(self, form):
        usuario = self.request.user
        user = authenticate(
            email=usuario.email,
            password=form.cleaned_data['password1']
        )
        if user is None:
            form.add_error(None, 'La contraseña actual es incorrecta.')
            return self.form_invalid(form)

        usuario.set_password(form.cleaned_data['password2'])
        usuario.save()
        logout(self.request)
        return super().form_valid(form)


class ListaUsuariosView(LoginRequiredMixin, ListView):
    template_name = 'users/lista_usuarios.html'
    context_object_name = 'usuarios'
    login_url = reverse_lazy('app_users:login')

    def get_queryset(self):
        return User.objects.all()


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'users/dashboard.html'
    login_url = reverse_lazy('app_users:login')
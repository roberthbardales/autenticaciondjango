from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
#
from .models import User

class AdministradorPermisoMixin(LoginRequiredMixin):
    login_url = reverse_lazy('app_users:login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.occupation != User.ADMINISTRADOR:
            return HttpResponseRedirect(reverse('app_users:login'))
        return super().dispatch(request, *args, **kwargs)


class DoctorPermisoMixin(LoginRequiredMixin):
    login_url = reverse_lazy('app_users:login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.occupation not in [User.ADMINISTRADOR, User.DOCTOR]:
            return HttpResponseRedirect(reverse('app_users:login'))
        return super().dispatch(request, *args, **kwargs)


class RecepcionPermisoMixin(LoginRequiredMixin):
    login_url = reverse_lazy('app_users:login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.occupation not in [User.ADMINISTRADOR, User.RECEPCION]:
            return HttpResponseRedirect(reverse('app_users:login'))
        return super().dispatch(request, *args, **kwargs)


class PacientePermisoMixin(LoginRequiredMixin):
    login_url = reverse_lazy('app_users:login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.occupation not in [User.ADMINISTRADOR, User.PACIENTE]:
            return HttpResponseRedirect(reverse('app_users:login'))
        return super().dispatch(request, *args, **kwargs)


# class ActiveAccountMixin(LoginRequiredMixin):
#     login_url = reverse_lazy('app_users:login')
#
#     def dispatch(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return self.handle_no_permission()
#         if not request.user.is_active:
#             return HttpResponseRedirect(reverse('app_users:login'))
#         return super().dispatch(request, *args, **kwargs)
#
#
# class StaffRequiredMixin(LoginRequiredMixin):
#     login_url = reverse_lazy('app_users:login')
#
#     def dispatch(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return self.handle_no_permission()
#         if not request.user.is_staff:
#             raise PermissionDenied
#         return super().dispatch(request, *args, **kwargs)
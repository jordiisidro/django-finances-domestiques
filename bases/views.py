from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy



class MixinFormInvalid:
    def form_invalid(self,form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response


class SensePrivilegis(LoginRequiredMixin, PermissionRequiredMixin, MixinFormInvalid):
    login_url = 'bases:login'
    raise_exception=False
    redirect_field_name ="redirect_to"

    def handle_no_permission(self):
        from django.contrib.auth.models import AnonymousUser
        if not self.request.user==AnonymousUser():
            self.login_url='bases:sense_privilegis'
        return HttpResponseRedirect(reverse_lazy(self.login_url))

class Home(LoginRequiredMixin, generic.TemplateView):
    #template_name='bases/home.html'
    template_name='moviment/moviment_dashboard.html'
    login_url ='bases:login'

class HomeSensePrivilegis(LoginRequiredMixin, generic.TemplateView):
    template_name='bases/sense_privilegis.html'
    login_url ='bases:login'

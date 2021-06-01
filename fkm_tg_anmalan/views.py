import csv

from django.apps import apps
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, ListView
from django.contrib.auth import login as auth_login, logout as auth_logout

import fkm_tg_anmalan.mixins as mixins
import fkm_tg_anmalan.forms as forms
import fkm_tg_anmalan.models as models


# Create your views here.
class Index(mixins.SiteMixin, TemplateView):
    pass


class Rooms(mixins.SiteMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'room_list': models.Room.objects.all()
        })
        if self.request.user.is_authenticated:
            context.update({
                'user_room_id': self.request.user.room.pk if self.request.user.room else -1
            })
        return context

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if 'logout' in self.request.POST:
                auth_logout(self.request)

            elif 'room' in self.request.POST:
                room_nr = int(self.request.POST['room'])
                if self.request.user.room is not None and room_nr == self.request.user.room.pk:
                    self.request.user.room = None
                else:
                    room = models.Room.objects.filter(pk=room_nr)
                    if len(room) == 1:
                        room = room[0]
                        if room.num_of_attendees < room.max_participants:
                            self.request.user.room = room

                self.request.user.save()

        return self.get(request, *args, **kwargs)


class SignUp(mixins.SiteMixin, FormView):
    form_class = forms.SignUpForm
    success_url = reverse_lazy('rum')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user.is_authenticated:
            kwargs.update({
                'instance': self.request.user
            })
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        if 'room_nr' in self.kwargs:
            initial['room'] = self.kwargs['room_nr']
        return initial

    def form_valid(self, form):
        user = form.instance
        user.save()
        if not user.got_login_details:
            user.send_signup_email()
        if not self.request.user.is_authenticated:
            auth_login(self.request, user)

        return super().form_valid(form)


class Login(mixins.SiteMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'SERVER_EMAIL': settings.SERVER_EMAIL
        })
        return context

    def get(self, request, *args, **kwargs):
        users = apps.get_model(settings.AUTH_USER_MODEL).objects.filter(username=kwargs['username'])
        if len(users) == 1:
            auth_login(request, users[0])
            return redirect('rum')
        else:
            return super(Login, self).get(request, *args, **kwargs)


def download(request):
    if request.user.is_authenticated and request.user.is_superuser:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="anmalda.csv"'

        writer = csv.writer(response)
        writer.writerow(['Namn', 'E-postadress', 'Årskurs', 'Rum', 'Märke', 'Gyckla', 'Gyckelkommentar', 'Med på bild'])
        for user in models.TGUser.objects.all():
            writer.writerow([str(user), user.email, user.year, user.room, user.patch, user.gyckla, user.gyckel_comment, user.on_photo])
        return response
    else:
        return HttpResponse()

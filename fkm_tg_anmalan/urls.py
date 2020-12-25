from django.conf import settings
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.shortcuts import redirect
from django.urls import include, path
from django.conf.urls.static import static
import fkm_tg_anmalan.views as views


urlpatterns = [
    path('', views.Index.as_view(
        template_name='fkm_tg_anmalan/index.html',
        site_name="Index",
        site_texts=['title', 'valkommen_text', 'youtube_link'],
        site_images=['banner']),
         name='index'),
    path('meny/', views.Index.as_view(
        template_name='fkm_tg_anmalan/menu.html',
        site_name="Meny",
        site_texts=['title', 'intro'],
        site_images=['menu'],
        site_files=['menu_pdf']),
         name='meny'),
    path('rum/', views.Rooms.as_view(
        template_name='fkm_tg_anmalan/rooms.html',
        site_name="Lista över rum",
        site_texts=['title', 'intro', 'logged_in', 'logged_out']),
         name='rum'),
    path('anmalan/<int:room_nr>/', views.SignUp.as_view(
        template_name='fkm_tg_anmalan/sign-up.html',
        site_name="Anmälan",
        site_texts=['title', 'intro', 'post_form_text']),
         name='anmalan'),
    path('anmalan/', views.SignUp.as_view(
        template_name='fkm_tg_anmalan/sign-up.html',
        site_name="Anmälan",
        site_texts=['title', 'intro', 'post_form_text']),
         name='anmalan'),
    path('login/<slug:username>/', views.Login.as_view(
        template_name='fkm_tg_anmalan/login-failed.html',
    ), name='login'),
    path('ladda-ned/', views.download, name='ladda-ned')
]

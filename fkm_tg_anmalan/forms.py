from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Hidden, Field
from django import forms
from django.apps import apps
from django.conf import settings
from django.forms.widgets import RadioSelect

import fkm_tg_anmalan.models as models

class SignUpForm(forms.ModelForm):
    class Meta:
        model = apps.get_model(settings.AUTH_USER_MODEL)
        fields = ['first_name', 'last_name', 'email', 'year', 'room', 'gyckla', 'gyckel_comment', 'patch', 'on_photo']

    def __init__(self, **kwargs):
        helper = FormHelper()
        helper.form_method = 'post'
        helper.form_tag = True
        helper.layout = Layout(
            Row(Column('first_name'), Column('last_name')),
            Row(Column('email'), Column()),
            Row(Column('year'), Column()),
            Row(Column('gyckla')),
            Field('gyckel_comment', rows=2),
            Row(Column('patch')),
            Row(Column('on_photo'))
        )
        if ('initial' in kwargs and 'room' in kwargs['initial']):
            helper.layout.append(Hidden('room', kwargs['initial']['room']))

        helper.layout.append(Submit('submit', 'Skicka'))

        self.helper = helper
        super().__init__(**kwargs)

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

        self.fields['gyckla'].widget = RadioSelect()
        self.fields['gyckla'].required = True
        self.fields['gyckla'].initial = None


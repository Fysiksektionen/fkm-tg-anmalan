from django.apps import apps
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import SET_NULL
from django.template.loader import get_template
from django.urls import reverse
from django.utils.crypto import get_random_string

from django.utils.translation import gettext_lazy as _
from .room import Room


# Create your models here.
class TGUser(AbstractUser):
    """
    Extension class of Django user to add user type and unique url code.
    """

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    first_name = models.CharField(_('first name'), max_length=30, blank=False, null=False)
    last_name = models.CharField(_('last name'), max_length=150, blank=False, null=False)
    email = models.EmailField(_('email address'), blank=False, null=False, unique=True)

    year = models.CharField(
        blank=True, null=True, max_length=15,
        verbose_name="Årskurs",
        help_text="Endast för fysiker."
    )

    room = models.ForeignKey(
        Room, on_delete=SET_NULL, null=True, blank=True, related_name="attendees",
        verbose_name="Rum",
        help_text="Du kan alltid byta rum i efterhand via länk du får per mejl."
    )

    gyckla = models.BooleanField(
        null=False, default=0,
        verbose_name="Jag vill gyckla under kvällen"
    )
    gyckel_comment = models.TextField(
        null=True, blank=True,
        verbose_name="Kommentar till gyckel",
        help_text="Här kan du skriva saker som kan vara bra för arrangören att veta."
                  "Medgycklare, om det kräver udda tekniska lösningar, etc."
    )

    on_photo = models.BooleanField(
        null=False, default=0,
        verbose_name="Jag accepterar att vara med på foton från kvällen.",
        help_text="Under det här arrangemanget tar vi bilder som sparas och sedan publiceras offentligt via "
                  "Fysiksektionens kommunikationskanaler. Om du motsätter dig denna behandling kan vi komma att "
                  "behöva ta en bild på dig för att i efterhand kunna säkerställa att inga bilder sparas. "
                  "Det går alltid att be om att vi plockar bort enskilda bilder. Är det okej att vi sparar och "
                  "sprider bilder på dig?"
    )

    patch = models.BooleanField(
        null=False, default=False,
        verbose_name="Jag vill köpa ett märke (15 kr)",
        help_text="Genom att fyll i detta först jag att jag är betalningsskyldig för detta märke."
    )

    got_login_details = models.BooleanField(verbose_name="Har fått inloggningsdetaljer", null=False, default=False)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def send_signup_email(self):
        """ (!) Only call this post save to db. """
        self.save()

        subject_template = get_template('fkm_tg_anmalan/email/bekraftelse_epost_amne.txt')
        plaintext = get_template('fkm_tg_anmalan/email/bekraftelse_epost.txt')
        html = get_template('fkm_tg_anmalan/email/bekraftelse_epost.html')

        context = {
            'link': settings.DOMAIN_URL + reverse('login', kwargs={'username': self.username})
        }

        from_email, to = None, str(self.email)
        subject = subject_template.render(context)
        text_content = plaintext.render(context)
        html_content = html.render(context)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")

        res = msg.send()
        if res == 1:
            self.got_login_details = True
            self.save()
            return True
        else:
            return False

    @property
    def user_tag(self):
        if self.year:
            if self.year < 14:
                return "F-Gammal"
            else:
                return "F-%02d" % self.year
        else:
            return "Extern"


def init_auto_fields(sender, instance, **kwargs):
    if not instance.username:
        username = None
        while username is None or username in TGUser.objects.values_list('username', flat=True):
            username = get_random_string(32)
        instance.username = username

    if not instance.password:
        instance.set_unusable_password()


def check_room_status(sender, instance, **kwargs):
    if 0 not in [room.attendees.count() for room in Room.objects.all()]:
        room = Room()
        room.save()


models.signals.pre_save.connect(init_auto_fields, sender=TGUser)
models.signals.post_save.connect(check_room_status, sender=TGUser)

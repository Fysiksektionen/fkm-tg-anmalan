from django.conf import settings
from django.db import models


def get_max():
    return settings.ROOM_MAX

# Create your models here.
class Room(models.Model):
    """
    Class representing a Zoom room.
    """

    max_participants = models.PositiveSmallIntegerField(verbose_name="Maximalt antal deltagare", default=get_max)
    special_name = models.CharField(max_length=50, verbose_name="Specialnamn", null=True, blank=True)

    class Meta:
        verbose_name = "Rum"
        verbose_name_plural = "Rum"

    def __str__(self):
        return "Rum %d" % self.pk

    @property
    def num_of_attendees(self):
        return self.attendees.count()

    @property
    def name(self):
        if self.special_name is not None:
            return self.special_name
        else:
            num_of_special_names = Room.objects.filter(pk__lt=self.pk).exclude(special_name=None).count()
            if len(settings.ROOM_NAMES) >= self.pk - num_of_special_names:
                return "%s rummet" % settings.ROOM_NAMES[self.pk - 1 - num_of_special_names]
            else:
                return str(self)

from django.conf import settings
from django.db import models


def get_max():
    return settings.ROOM_MAX


class Room(models.Model):
    """
    Class representing a Zoom room.
    """

    max_participants = models.PositiveSmallIntegerField(verbose_name="Maximalt antal deltagare", default=get_max)
    name = models.CharField(max_length=50, verbose_name="Namn", null=False, blank=False, unique=True)

    class Meta:
        verbose_name = "Rum"
        verbose_name_plural = "Rum"

    def __str__(self):
        return "Rum %d" % self.pk

    @property
    def num_of_attendees(self):
        return self.attendees.count()

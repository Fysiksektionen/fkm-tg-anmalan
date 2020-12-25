from django.apps import apps
from django.conf import settings
from django.contrib import admin
import fkm_tg_anmalan.models as models
# Register your models here.


@admin.register(apps.get_model(settings.AUTH_USER_MODEL))
class UserAdmin(admin.ModelAdmin):
    ordering = ['first_name', 'last_name']
    list_display = ['__str__', 'email', 'year', 'room']
    list_filter = ['year', 'room']


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    ordering = ['pk']
    list_display = ['name', 'pk', 'num_of_attendees']


class SiteTextAdmin(admin.TabularInline):
    model = models.SiteText
    extra = 0
    readonly_fields = ('key',)
    fields = ('key', 'text')

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class SiteImageAdmin(admin.TabularInline):
    model = models.SiteImage
    extra = 0
    readonly_fields = ('key',)
    fields = ('key', 'image')

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class SiteFileAdmin(admin.TabularInline):
    model = models.SiteFile
    extra = 0
    readonly_fields = ('key',)
    fields = ('key', 'file')

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class SiteParagraphAdmin(admin.StackedInline):
    model = models.SiteParagraph
    extra = 0
    fields = ('order_num', 'title', 'text', 'image')

    def has_add_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)


class SiteParagraphListAdmin(admin.ModelAdmin):
    fields = ('key', 'site', 'ascending_order')
    readonly_fields = ('key', 'site')
    inlines = [SiteParagraphAdmin]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'number_of_texts', 'number_of_images', 'number_of_files', 'number_of_lists')
    inlines = [SiteTextAdmin, SiteImageAdmin, SiteFileAdmin]
    readonly_fields = ('name',)
    fields = ('name',)

    def number_of_texts(self, obj):
        return obj.texts.all().count()

    def number_of_images(self, obj):
        return obj.images.all().count()

    def number_of_files(self, obj):
        return obj.files.all().count()

    def number_of_lists(self, obj):
        return obj.paragraph_lists.all().count()

    def has_add_permission(self, obj):
        return False

    def get_inlines(self, request, obj):
        inlines = []
        if self.number_of_texts(obj):
            inlines.append(SiteTextAdmin)
        if self.number_of_images(obj):
            inlines.append(SiteImageAdmin)
        if self.number_of_files(obj):
            inlines.append(SiteFileAdmin)
        return inlines


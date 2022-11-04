from django.contrib import admin
from django import forms


from news import models


class PublicationGalleryAdmin(admin.StackedInline):
    model = models.PublicationGallery


class PublicationForm(forms.ModelForm):

    class Meta:
        model = models.Publication
        fields = "__all__"


@admin.register(models.Publication)
class PublicationAdmin(admin.ModelAdmin):
    form = PublicationForm
    inlines = [PublicationGalleryAdmin]


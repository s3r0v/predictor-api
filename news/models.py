from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile, File
from django.template.defaultfilters import slugify
from utils.models import MixinDateModel
from unidecode import unidecode
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.


class Publication(MixinDateModel):

    image = models.ImageField(
        upload_to="publications", blank=True, null=True, verbose_name="Картинка"
    )
    title = models.CharField(max_length=128, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    slug = models.SlugField(verbose_name="Слаг", blank=True, null=True)
    content = RichTextUploadingField(blank=True, null=True, verbose_name="Контент")
    isVisible = models.BooleanField(blank=True, null=True, verbose_name="Видимая?")
    inSlider = models.BooleanField(blank=True, null=True, verbose_name="Выводить в слайдер?")
    availableUntill = models.DateTimeField(
        blank=True, null=True, verbose_name="Доступна до"
    )

    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        super(Publication, self).save(*args, **kwargs)

class PublicationGallery(MixinDateModel):
    publication = models.ForeignKey(
        Publication, on_delete=models.CASCADE, verbose_name="Публикация"
    )
    image = models.ImageField(upload_to="publications/gallery", verbose_name="Картинка")
    desc = models.TextField(verbose_name="Описание")

    class Meta:
        verbose_name = "Галерея публикации"
        verbose_name_plural = "Галереи публикаций"

    def save(self, *args, **kwargs):
        super(PublicationGallery, self).save(*args, **kwargs)

    def __str__(self):
        return f"Галерея публикации {self.publication.title}"

from django.db import models
from django.core.validators import ValidationError


class Prediction(models.Model):
    data = models.JSONField(blank=True, null=True, verbose_name='Prediction')
    
    class Meta:
        verbose_name = 'Prediction'
        verbose_name_plural = 'Predictions'

    def save(self, *args, **kwargs):
        if not self.pk and Prediction.objects.exists():
            raise ValidationError('Prediction page can only be sole')
        super(Prediction, self).save(*args, **kwargs)

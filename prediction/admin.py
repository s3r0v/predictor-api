from django.contrib import admin
from prediction import models


@admin.register(models.Prediction)
class PredictionAdmin(admin.ModelAdmin):
    inlines = []

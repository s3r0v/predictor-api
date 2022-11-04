from django.contrib import admin
from tradesData import models


@admin.register(models.Kline)
class KlineAdmin(admin.ModelAdmin):
    inlines = []
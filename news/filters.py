from django_filters import rest_framework as filters

from news import models


class PublicationFilter(filters.FilterSet):
    class Meta:
        model = models.Publication
        fields = ["inSlider"]

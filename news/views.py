from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from news import serializers, models, filters


class PublicationDetailView(generics.RetrieveAPIView):
    queryset = models.Publication.objects.all()
    serializer_class = serializers.PublicationDetailSerializer
    lookup_field = "slug"


class PublicationListView(generics.ListAPIView):
    queryset = models.Publication.objects.filter(isVisible=True).order_by("createdAt")
    serializer_class = serializers.PublicationListSerializer

    pagination_class = LimitOffsetPagination

    filterset_class = filters.PublicationFilter
    filter_backends = [DjangoFilterBackend]
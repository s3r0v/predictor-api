from rest_framework import serializers

from news import models


class PublicationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Publication
        fields = ["id", "category", "title", "description", "createdAt", 'slug', "inSlider", "image"]


class PublicationGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PublicationGallery
        fields = ["image", "desc"]


class PublicationDetailSerializer(serializers.ModelSerializer):
    gallery = PublicationGallerySerializer(many=True, source="publicationgallery_set")
    text = serializers.CharField(source="content")

    class Meta:
        model = models.Publication
        fields = [
            "id",
            "category",
            "title",
            "description",
            "createdAt",
            "text",
            "gallery",
            "inSlider",
            "image",
            "slug",
        ]

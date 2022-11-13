from rest_framework import serializers
from prediction import models


class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Prediction
        fields = ["data"]
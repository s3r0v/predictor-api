from django.views.decorators.csrf import csrf_exempt

from auth.backends import VerifyRequest
from rest_framework import viewsets
from prediction import models, serializers


# Create your views here.

class GetPrediction(viewsets.ModelViewSet):
    queryset = models.Prediction.objects.all()
    serializer_class = serializers.PredictionSerializer
    permission_classes = [VerifyRequest]

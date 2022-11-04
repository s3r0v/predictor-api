from django.urls import path
from prediction import views

app_name = "prediction"

urlpatterns = [
    path("", views.GetPrediction.as_view({'get': 'list'}), name="getPrediction"),
]

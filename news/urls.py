from django.urls import path

from news import views

app_name = "news"

urlpatterns = [
    path("", views.PublicationListView.as_view(), name="publication_list"),
    path(
        "<str:slug>",
        views.PublicationDetailView.as_view(),
        name="publication_detail",
    ),
]

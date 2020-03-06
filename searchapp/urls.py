from django.urls import path
from .views import SearchIdView,SearchFieldView

urlpatterns = [
    path("movies/<slug:id>/",SearchIdView.as_view(),name="search_id"),
    path("movies/", SearchFieldView.as_view(), name="search_field")
]

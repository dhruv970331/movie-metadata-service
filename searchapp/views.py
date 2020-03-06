from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .database import Movies
from django.http import JsonResponse
# Create your views here.


class SearchIdView(APIView):
    def get(self, request, id):
        movie = Movies.catalog.search_by_id(id)
        return JsonResponse(movie)


class SearchFieldView(APIView):
    def get(self, request):
        kwargs = {k: v for k, v in request.GET.items()}
        data = Movies.catalog.filter(**kwargs)
        return JsonResponse({"success": True, "data": data})

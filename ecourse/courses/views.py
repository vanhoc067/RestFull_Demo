from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions, generics
from .models import Category, Course
from .serializers import CategorySerializer, CourseSerializer


def index(request):
    return HttpResponse('Hello World!!!')


def test(request):
    return render(request, 'test.html',{
        'name' : 'Hoc'
    })


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.filter(active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query = self.queryset

        kw = self.request.query_params.get('kw')
        if kw:
            query = query.filter(name__icontains=kw)

        return query


class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Course.objects.filter(active=True)
    serializer_class = CourseSerializer
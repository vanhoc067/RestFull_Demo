from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions
from .models import Course
from .serializers import CourseSerializer


def index(request):
    return HttpResponse('Hello World!!!')


def test(request):
    return render(request, 'test.html',{
        'name' : 'Hoc'
    })


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.filter(active=True)
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse('Hello World!!!')


def test(request):
    return render(request, 'test.html',{
        'name' : 'Hoc'
    })

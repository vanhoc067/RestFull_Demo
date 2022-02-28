from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='course_index'),
    path('test/', views.test, name='course_test')
]



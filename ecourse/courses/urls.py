from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(prefix='categories', viewset=views.CategoryViewSet, basename="category")
router.register(prefix='course', viewset=views.CourseViewSet, basename='course')

urlpatterns = [
    # path('', views.index, name='course_index'),
    path('', include(router.urls)),
    path('test/', views.test, name='course_test')
]






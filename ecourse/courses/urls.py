from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register('courses', views.CourseViewSet)

urlpatterns = [
    # path('', views.index, name='course_index'),
    path('', include(router.urls)),
    path('test/', views.test, name='course_test')
]






import int as int
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Course, Lesson, Comment, User, Like, Rating
from .serializers import (CategorySerializer, CourseSerializer,
                          CoursePaginator, LessonSerializer,
                          LessonDetailSerializer, CommentSerializer,
                          CreateCommentsSerializer, UserSerializer)
from drf_yasg.utils import swagger_auto_schema


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
    pagination_class = CoursePaginator

    def get_queryset(self):
        query = self.queryset

        kw = self.request.query_params.get('kw')
        if kw:
            query = query.filter(subject__icontains=kw)

        cate_id = self.request.query_params.get('category_id')
        if cate_id:
            query = query.filter(category_id=cate_id)

        return query

    @action(methods=['get'], detail=True, url_path='lessons')
    def get_lessons(self, request, pk):
        course = self.get_object()
        lessons = course.lessons.filter(active=True)
        kw = request.query_params.get('kw')
        if kw:
            lessons = lessons.filter(subject__icontains=kw)

        return Response(data=LessonSerializer(lessons, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)


class LessonViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Lesson.objects.filter(active=True)
    serializer_class = LessonDetailSerializer

    def get_permissions(self):
        if self.action in ['like', 'rating']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @swagger_auto_schema(
        operation_description='Get the comments og Lesson',
        responses={
            status.HTTP_200_OK: CommentSerializer()
        }
    )
    @action(methods=['get'], url_path='comments', detail=True)
    def get_comments(self, request, pk):
        lesson = self.get_object()
        comments = lesson.comment.select_related('user').filter(active=True)

        return Response(CommentSerializer(comments, many=True).data, status=status.HTTP_200_OK)

    @action(methods=['post'], url_path='like', detail=True)
    def like(self, request, pk):
        lesson = self.get_object()
        user = request.user #lấy user đã chứng thực đang đăng nhập

        l, _ = Like.objects.get_or_create(lesson=lesson, user=user)  #vừa update vừa tạo mới Like
        l.active = not l.active
        l.save()

        return Response(status=status.HTTP_201_CREATED)

    @action(methods=['post'], url_path='rating', detail=True)
    def rating(self, request, pk):
        if 'rate' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        lesson = self.get_object()
        user = request.user

        r, _ = Rating.objects.get_or_create(lesson=lesson, user=user)
        r.rate = request.data.get('rate')
        r.save()

        return Response(status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ViewSet, generics.ListAPIView,generics.CreateAPIView):
    queryset = Comment.objects.filter(active=True)
    serializer_class = CreateCommentsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permission(self):
        if self.action in ['update', 'delete']:
            # request.user
            # request.data.user
            pass

        return [permissions.IsAuthenticated()]


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer


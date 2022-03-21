from rest_framework import serializers, pagination
from .models import Category, Course, Lesson, Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image')

    def get_image(self, obj):
        request = self.context['request']
        if obj.image and not obj.image.name.startswith('/static'):
            path = '/static/%s' % obj.image.name

            return request.build_absolute_uri(path)

    class Meta:
        model = Course
        fields = ['id', 'subject', 'image', 'created_date', 'category_id']


class CoursePaginator(pagination.PageNumberPagination):
    page_size = 2
    page_query_param = 'page'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class LessonSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image')
    tags = TagSerializer(many=True)

    def get_image(self, obj):
        request = self.context['request']
        if obj.image and not obj.image.name.startswith('/static'):
            path = '/static/%s' % obj.image.name

            return request.build_absolute_uri(path)

    class Meta:
        model = Lesson
        fields = ['id', 'subject', 'created_date', 'update_date', 'course_id', 'image', 'tags']


class LessonDetailSerializer(LessonSerializer):
    class Meta:
        model = Lesson
        fields = LessonSerializer.Meta.fields + ['content']

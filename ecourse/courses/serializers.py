from rest_framework import serializers, pagination
from .models import Category, Course, Lesson, Tag, Comment, User


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
        fields = ['id', 'subject', 'created_date', 'update_date', 'course_id', 'image', 'tags', 'like']


class LessonDetailSerializer(LessonSerializer):
    like = serializers.SerializerMethodField()

    def get_like(self, obj):
        request = self.context['request']
        if request.user.is_authenticated:
            return obj.like_set.filter(user=request.user,
                                       active=True).exists()  # phương thức exists trả về đối tượng true/false

    class Meta:
        model = Lesson
        fields = LessonSerializer.Meta.fields + ['content']


class UserSerializer(serializers.ModelSerializer):
    avatar_path = serializers.SerializerMethodField(source='avatar')

    def get_avatar_path(self, obj):
        request = self.context['request']
        if obj.avatar and not obj.avatar.name.startswith('/static'):
            path = '/static/%s' % obj.avatar.name

            return request.build_absolute_uri(path)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'avatar', 'password', 'avatar_path']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'avatar_path': {
                'read_only': True
            },
            'avatar': {
                'write_only': True
                }

        }

    def create(self, validated_date):
        data = validated_date.copy()

        u = User(**data)
        u.set_password(u.password)
        u.save()

        return u


class CreateCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'user', 'lesson']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        exclude = ['active']




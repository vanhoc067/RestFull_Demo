from django.contrib import admin
from .models import User, Category, Course, Lesson, Tag
from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Lesson
        fields = '__all__'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'active', 'created_date')
    list_filter = ('id', 'name', 'created_date')
    search_fields = ('id', 'name')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('subject', 'description', 'image', 'category')



class LessonAdmin(admin.ModelAdmin):
    readonly_fields = ['image_view']
    form = LessonForm

    def image_view(self, Lesson):
        if Lesson:
            return mark_safe(
                '<img src="/static/{url}" width="120" />' \
                    .format(url=Lesson.image.name))



admin.site.register(User)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Tag)
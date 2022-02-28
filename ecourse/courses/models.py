from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class ModelBase(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True #Tạo lớp trường tượng


class Category(ModelBase):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Course(ModelBase):
    subject = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ('subject', 'category')


# Create your models here.

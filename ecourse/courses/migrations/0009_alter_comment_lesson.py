# Generated by Django 4.0.2 on 2022-03-26 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_alter_comment_lesson_alter_comment_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='courses.lesson'),
        ),
    ]

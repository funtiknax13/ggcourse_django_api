# Generated by Django 4.2.4 on 2023-08-29 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='название курса')),
                ('description', models.TextField(verbose_name='описание курса')),
                ('image', models.ImageField(upload_to='course/course', verbose_name='превью курса')),
            ],
            options={
                'verbose_name': 'Курс',
                'verbose_name_plural': 'Курсы',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='название урока')),
                ('description', models.TextField(verbose_name='описание урока')),
                ('image', models.ImageField(upload_to='course/lesson', verbose_name='превью урока')),
                ('video_link', models.CharField(max_length=500, verbose_name='ссылка на видео')),
            ],
            options={
                'verbose_name': 'Урок',
                'verbose_name_plural': 'Уроки',
            },
        ),
    ]

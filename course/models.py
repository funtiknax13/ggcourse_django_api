from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name='название курса')
    description = models.TextField(verbose_name='описание курса')
    image = models.ImageField(upload_to='course/course', verbose_name='превью курса')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name='название урока')
    description = models.TextField(verbose_name='описание урока')
    image = models.ImageField(upload_to='course/lesson', verbose_name='превью урока')
    video_link = models.CharField(max_length=500, verbose_name='ссылка на видео')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

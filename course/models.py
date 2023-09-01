from django.db import models

from users.models import User

NULLABLE = {'null': True, 'blank': True}


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
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, verbose_name='курс', **NULLABLE)
    title = models.CharField(max_length=100, verbose_name='название урока')
    description = models.TextField(verbose_name='описание урока')
    image = models.ImageField(upload_to='course/lesson', verbose_name='превью урока')
    video_link = models.CharField(max_length=500, verbose_name='ссылка на видео')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'наличные'),
        ('card', 'карта'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    date = models.DateField(verbose_name='дата платежа')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='урок', **NULLABLE)
    amount = models.PositiveIntegerField(verbose_name='сумма оплаты')
    method = models.CharField(max_length=25, choices=PAYMENT_METHODS, verbose_name='методы оплаты')

    def __str__(self):
        return f'{self.course.title if self.course else self.lesson.title} - {self.amount} руб. ({self.user.email} / {self.date})'

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'


from django.contrib import admin

from course.models import Course, Lesson, Payment, Subscription
from users.models import User

# Register your models here.

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Payment)
admin.site.register(User)
admin.site.register(Subscription)

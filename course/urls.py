from django.urls import path

from course.apps import CourseConfig
from rest_framework.routers import DefaultRouter

from course.views import LessonListAPIView, LessonCreateAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PaymentListAPIView, CourseListAPIView, CourseCreateAPIView, \
    CourseRetrieveAPIView, CourseUpdateAPIView, CourseDestroyAPIView

app_name = CourseConfig.name

router = DefaultRouter()
# router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('course/', CourseListAPIView.as_view(), name='course-list'),
    path('course/create/', CourseCreateAPIView.as_view(), name='course-create'),
    path('course/<int:pk>/', CourseRetrieveAPIView.as_view(), name='course-detail'),
    path('course/<int:pk>/update/', CourseUpdateAPIView.as_view(), name='course-update'),
    path('course/<int:pk>/delete/', CourseDestroyAPIView.as_view(), name='course-delete'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-detail'),
    path('lesson/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson-delete'),
    path('payment/', PaymentListAPIView.as_view(), name='payment-list'),

] + router.urls

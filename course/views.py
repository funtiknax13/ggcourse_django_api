import datetime

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from course.models import Course, Lesson, Payment, Subscription
from course.paginators import CoursePaginator, LessonPaginator
from course.permissions import IsNotModerator, IsOwnerOrModerator
from course.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer
from course.services import create_payment
from course.tasks import send_course_update_message


class CourseCreateAPIView(generics.CreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsNotModerator, ]

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModerator]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class CourseListAPIView(generics.ListAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, ]
    pagination_class = CoursePaginator


class CourseRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]


class CourseUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]

    def update(self, request, *args, **kwargs):
        course = Course.objects.get(pk=kwargs['pk'])
        subscribers = Subscription.objects.filter(course=course)
        subscribers_email = []
        for subscriber in subscribers:
            subscribers_email.append(subscriber.user.email)
        message = f'Курс "{course.title}" обновлен'
        send_course_update_message.delay('Обновление курса', message, subscribers_email)
        return super().update(request, *args, **kwargs)


class CourseDestroyAPIView(generics.DestroyAPIView):
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator, IsNotModerator]


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ]
    pagination_class = LessonPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator, IsNotModerator]


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        """
            Subscribe for the course.
            ---
            parameters:
            - id: course_id
            """
        user = request.user
        course = Course.objects.get(pk=pk)
        is_subscription = Subscription.objects.filter(user=user, course=course).exists()
        if is_subscription:
            Subscription.objects.filter(user=user, course=course).delete()
            return Response({'status': f'You have unsubscribed from the course - {course.title}'})
        else:
            subscription = Subscription.objects.create(user=user, course=course)
            subscription.save()
            return Response({'status': f'You have subscribed for the course - {course.title}'})


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'method')
    ordering_fields = ('date', )
    permission_classes = [IsAuthenticated, ]


class PaymentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk):
        """
            Pay for the course.
            ---
            parameters:
            - id: course_id
        """
        course = Course.objects.get(pk=pk)
        price = 2000
        response = create_payment(course, price)
        if response:
            Payment.objects.create(user=request.user,
                                   date=datetime.date.today(),
                                   course=course,
                                   method='card',
                                   amount=price/100)
            return Response({'payment_url': response})
        else:
            return Response({'error': 'Ошибка платежа'})



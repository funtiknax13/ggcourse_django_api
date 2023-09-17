from rest_framework import serializers

from course.models import Course, Lesson, Payment, Subscription
from course.validators import VideoValidator


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [VideoValidator(field='video_link'), ]


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField(read_only=True)
    lessons = LessonSerializer(source='lesson_set', read_only=True, many=True)
    subscription = serializers.SerializerMethodField()

    @staticmethod
    def get_lesson_count(obj):
        return obj.lesson_set.count()

    def get_subscription(self, obj):
        request = self.context.get('request')
        for subscription in obj.subscription_set.all():
            if request.user == subscription.user:
                return True
        return False

    class Meta:
        model = Course
        fields = ['owner', 'title', 'description', 'image', 'lesson_count', 'lessons', 'subscription']


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'





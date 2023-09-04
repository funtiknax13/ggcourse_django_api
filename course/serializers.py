from rest_framework import serializers

from course.models import Course, Lesson, Payment


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', read_only=True, many=True)

    @staticmethod
    def get_lesson_count(obj):
        return obj.lesson_set.count()

    class Meta:
        model = Course
        fields = ['title', 'description', 'image', 'lesson_count', 'lessons']


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'





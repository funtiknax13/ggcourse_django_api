from rest_framework import status
from rest_framework.test import APITestCase

from course.models import Course, Lesson, Subscription
from users.models import User


# Create your tests here.
class LessonTestCase(APITestCase):

    def setUp(self) ->None:
        self.user = User.objects.create(
            email='test@test.com'
        )
        self.user.set_password('1234')
        self.user.save()

        self.course = Course.objects.create(
            title='TestCourse', description='TestCourseDescription'
        )

        self.lesson = Lesson.objects.create(
            title='TestLesson',
            description='TestLessonDescription',
            video_link='https://www.youtube.com',
            owner=self.user,
            course=self.course,
        )

    def test_create_lesson(self):
        """ Тестирование создания урока """
        data = {
            'title': 'Тестовый урок',
            'description': 'Описание тестового урока',
            'video_link': 'https://www.youtube.com',
            'course': self.course.pk
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            '/lesson/create/',
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Lesson.objects.all().exists(),
            {'id': 2, 'title': 'Тестовый урок', 'description': 'Описание тестового урока',
             'image': None, 'video_link': 'https://www.youtube.com', 'owner': 1, 'course': 1}
        )

    def test_list_lesson(self):
        """Тестирование вывода списка уроков"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            '/lesson/',
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        # print(response.json().get("results"))
        self.assertEqual(
            response.json().get("results"),
            [{'id': self.lesson.pk, 'title': 'TestLesson', 'description': 'TestLessonDescription',
              'image': None, 'video_link': 'https://www.youtube.com', 'owner': self.user.pk, 'course': self.course.pk}]

        )

    def test_lesson_retrieve(self) -> None:
        self.client.force_authenticate(user=self.user)

        response = self.client.get(f'/lesson/{self.lesson.pk}/')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        response = response.json()

        self.assertEqual(response.get('title'), 'TestLesson')
        self.assertEqual(response.get('description'), 'TestLessonDescription')
        self.assertEqual(response.get('image'), None)
        self.assertEqual(response.get('video_link'), 'https://www.youtube.com')
        self.assertEqual(response.get('course'), self.course.pk)
        self.assertEqual(response.get('owner'), self.user.pk)

    def test_lesson_update(self):
        self.client.force_authenticate(user=self.user)

        data = {
            'title': 'TestLessonUpdated',
            'description': 'TestLessonDescriptionUpdated',
        }

        response = self.client.put(
            path=f'/lesson/{self.lesson.pk}/update/', data=data,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        response = response.json()

        self.assertEqual(response.get('title'), 'TestLessonUpdated')
        self.assertEqual(response.get('description'), 'TestLessonDescriptionUpdated')
        self.assertEqual(response.get('image'), None)
        self.assertEqual(response.get('video_link'), 'https://www.youtube.com')
        self.assertEqual(response.get('course'), self.course.pk)
        self.assertEqual(response.get('owner'), self.user.pk)

    def test_lesson_delete(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            f'/lesson/{self.lesson.pk}/delete/',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Lesson.objects.all().exists(),
        )

    def tearDown(self) -> None:
        self.user.delete()
        self.course.delete()
        self.lesson.delete()


class SubscriptionTestCase(APITestCase):

    def setUp(self) ->None:
        self.user = User.objects.create(
            email='test@test.com'
        )
        self.user.set_password('1234')
        self.user.save()

        self.course = Course.objects.create(
            title='TestCourse', description='TestCourseDescription'
        )

        self.course2 = Course.objects.create(
            title='TestCourse2', description='TestCourse2Description'
        )

        self.subscription = Subscription.objects.create(
            user=self.user,
            course=self.course2
        )

    def test_create_subscription(self):
        """ Тестирование создания подписки """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            f'/course/{self.course.pk}/subscribe/',
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        response = response.json()
        self.assertEqual(response.get('status'), 'You have subscribed for the course - TestCourse')

    def test_delete_subscription(self):
        """ Тестирование удаления подписки """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            f'/course/{self.course2.pk}/subscribe/',
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        response = response.json()
        self.assertEqual(response.get('status'), 'You have unsubscribed from the course - TestCourse2')

    def tearDown(self) -> None:
        self.user.delete()
        self.course.delete()
        self.course2.delete()
        self.subscription.delete()

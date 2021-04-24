import time

from django.test import TestCase
from django.contrib.auth.models import User
from tutorial.quickstart.models import Follow

# Create your tests here.


class UsersTestCase(TestCase):
    def test_simple(self):
        self.assertEqual(1 + 2, 3)

    def test_unknown_url(self):
        # Клиент к нашему серверу
        response = self.client.get('/incorrect')
        self.assertEqual(response.status_code, 404)

    def test_empty_list_users(self):
        response = self.client.get('/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "count": 0,
            "next": None,
            "previous": None,
            "results": []
        })

    # def test_list_users_with_users_usernames(self):
    #     User.objects.create(username='Elon')
    #     User.objects.create(username='Putin')
    #     response = self.client.get('/v1/users/')
    #     self.assertEqual(response.status_code, 200)
    #     usernames = {row['username'] for row in response.json()['results']}
    #     self.assertEqual(usernames, {'Elon', 'Navalny'})

    def test_list_users_with_users(self):
        User.objects.create(username='Putin')
        # time.sleep(0.001)
        User.objects.create(username='Elon')
        response = self.client.get('/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "email": "",
                        "first_name": "",
                        "last_name": "",
                        "url": "http://testserver/v1/users/Elon/",
                        "username": "Elon",
                    },
                    {
                        "email": "",
                        "first_name": "",
                        "last_name": "",
                        "url": "http://testserver/v1/users/Putin/",
                        "username": "Putin",
                    },
                ]
            }
        )


class FollowTestCase(TestCase):
    def setUp(self):  # подготовка данных
        self.user1 = User.objects.create(username='Kevin')
        self.user2 = User.objects.create(username='Tom')
        self.user3 = User.objects.create(username='Jerry')
        Follow.objects.create(follower=self.user1, follows=self.user2)

    def test_data_exists(self):
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(Follow.objects.count(), 1)

    def test_new_follow_correct(self):
        self.client.force_login(self.user1)
        response = self.client.post(f'/v1/follow/{self.user3.username}/')
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(Follow.objects.get(
            follower=self.user1,
            follows=self.user3,
        ))

    def test_unfollow_correct(self):
        self.client.force_login(self.user1)
        response = self.client.delete(f'/v1/follow/{self.user2.username}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Follow.objects.count(), 0)

    # Подписка второй раз
    def test_follow_duplicate_failed(self):
        self.client.force_login(self.user1)
        self.assertEqual(Follow.objects.count(), 1)
        response = self.client.post(f'/v1/follow/{self.user2.username}/')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Follow.objects.count(), 1)

    # Подписка на самого себя
    def test_follow_yourself_failed(self):
        self.client.force_login(self.user1)
        response = self.client.post(f'/v1/follow/{self.user1.username}/')
        self.assertEqual(response.status_code, 400)

    # Отписка от самого себя
    def test_unfollow_not_exists_return_fail(self):
        self.client.force_login(self.user1)
        response = self.client.delete(f'/v1/follow/{self.user1.username}/')
        self.assertEqual(response.status_code, 400)
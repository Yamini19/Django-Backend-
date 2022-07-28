


import email
from unicodedata import name
from webbrowser import get
from django.db import models
from django.contrib.auth.hashers import get_hasher
from django.test import TestCase
from UsersApp.models import User


class TestModels(TestCase):
    def setUp(self):
        self.User1 = User.objects.create(
            name='User1',
            email= 'User1@myndsoft.de',
            password = '1234',
            username = 'user1'
             )


    def test_User_name(self):
        self.assertEqual(self.User1.name, 'User1')


    def test_User_email(self):
        self.assertEqual(self.User1.email, 'User1@myndsoft.de')


    def test_User_password(self):
        self.assertEqual(self.User1.password, '1234')


    def test_User_username(self):
        self.assertEqual(self.User1.username, 'user1')


    def test_check_Password(self):
        User2 = User.objects.create(
            name = 'user2',
            email = 'User2@myndsoft.de',
            password = "b'784f07f58c463e699a1b7ef1a9536c26b020db59ce50956da02bc7a8cdf723c0'"
        )

        assert(User2.check_password('test'))

      



   

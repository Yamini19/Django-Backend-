from asyncio.base_subprocess import ReadSubprocessPipeProto
from sre_constants import SUCCESS
from unittest import mock
from urllib import response
from django.test import TestCase

from django.test import TestCase, Client
from django.urls import reverse
from UsersApp.models import User
from rest_framework.test import APITestCase
from rest_framework import status, serializers

class BaseTest(TestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_url = reverse('user')
        self.logout_url = reverse('logout')
        self.refresh_url = reverse('refresh')
        self.user= {
            "name": "Test",
            "email": "testemail@test.com",
            "username":"test",
            "password":"test"
        }
        self.user_invalidEmail= {
            "username": "incorrect",
            "email": "email@test.com",
            "password":"test"
        }
        self.user_wrongPassword= {
            "name": "Test",
            "email": "testemail@test.com",
            "username":"test",
            "password":"testing"
        }
        return super().setUp()

    
class RegisterTest(BaseTest):
    def test_can_register_user(self):
        response = self.client.post(self.register_url,self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class LoginTest(BaseTest):
    def test_login_success(self):
        self.client.post(self.register_url, self.user)
        user= User.objects.filter(username= self.user['username']).first()
        user.is_active= True
        user.save()
        response = self.client.post(self.login_url, self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_user_NotFound(self): #failed
        self.client.post(self.register_url, self.user)
        response = self.client.post(self.login_url, self.user_invalidEmail)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_login_wrongPassword(self): # failed
        self.client.post(self.register_url, self.user)
        user= User.objects.filter(username= self.user['username']).first()
        user.is_active= True
        user.save()
        response = self.client.post(self.login_url, self.user_wrongPassword)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserTest(BaseTest):
    def test_can_fetch_user_data(self):
        self.client.post(self.register_url, self.user)
        user= User.objects.filter(username= self.user['username']).first()
        user.is_active= True
        user.save()
        loginResponse= self.client.post(self.login_url, self.user)
        token = loginResponse.data['token'] 
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + token,
        }
        response = self.client.get(self.user_url, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_fetch_user_data(self): #failed
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class LogoutTest(BaseTest):
    def test_can_user_logout(self):
        self.client.post(self.register_url, self.user)
        user= User.objects.filter(username= self.user['username']).first()
        user.is_active= True
        user.save()
        self.client.post(self.login_url, self.user)
        response = self.client.post(self.logout_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        
class RefreshTokenTest(BaseTest):
    def test_gen_new_access_token(self):
        self.client.post(self.register_url, self.user)
        user= User.objects.filter(username= self.user['username']).first()
        user.is_active= True
        user.save()
        self.client.post(self.login_url, self.user)
        response = self.client.post(self.refresh_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
from django.test import SimpleTestCase
from django.urls import reverse,resolve
from UsersApp.views import RegisterAPIView, LoginAPIView, UserAPIView, LogoutAPIView



class TestUrls(SimpleTestCase):
    def test_register_url_resolves(self):
        url=reverse('register')
        self.assertEqual(resolve(url).func.view_class,RegisterAPIView)

    def test_login_url_resolves(self):
        url=reverse('login')
        self.assertEqual(resolve(url).func.view_class,LoginAPIView)


    def test_user_url_resolves(self):
        url=reverse('user')
        self.assertEqual(resolve(url).func.view_class,UserAPIView)


    def test_logout_url_resolves(self):
        url=reverse('logout')
        self.assertEqual(resolve(url).func.view_class,LogoutAPIView)

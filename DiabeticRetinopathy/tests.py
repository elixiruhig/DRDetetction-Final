import time
from unittest import TestCase

from django.core.exceptions import ValidationError
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from DiabeticRetinopathy import models, forms

class LoginTestCase(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Firefox()
        super(LoginTestCase, self).setUp()

    def tearDown(self):

        self.selenium.quit()
        super(LoginTestCase, self).tearDown()

    def test_login(self):
        selenium = self.selenium

        selenium.get('http://127.0.0.1:8000/')

        email = selenium.find_element_by_id('id_email')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_name('login')

        email.send_keys('admin2@admin.com')
        password.send_keys('pickpocket')
        submit.send_keys(Keys.RETURN)

        self.assertIn('http://127.0.0.1:8000/', self.selenium.current_url)
        #assert 'Login test successful\n' in selenium.page_source

class SignupTestCase(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Firefox()
        super(SignupTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(SignupTestCase, self).tearDown()

    def test_signup(self):
        selenium = self.selenium

        selenium.get('http://127.0.0.1:8000/')

        first_name = selenium.find_element_by_id('id_first_name')
        last_name = selenium.find_element_by_id('id_last_name')
        oname = selenium.find_element_by_id('id_oname')
        email = selenium.find_element_by_id('id_email')
        bdate = selenium.find_element_by_id('id_bdate')
        password1 = selenium.find_element_by_id('id_password1')
        password2 = selenium.find_element_by_id('id_password2')
        submit = selenium.find_element_by_name('register')

        first_name.send_keys('test')
        last_name.send_keys('user')
        oname.send_keys('SKNCOE')
        email.send_keys('test@test.com')
        bdate.send_keys('20-08-1989')
        password1.send_keys('adminadmin')
        password2.send_keys('adminadmin')
        submit.send_keys(Keys.RETURN)

        self.assertIn('http://127.0.0.1:8000/', self.selenium.current_url)
        #assert 'Signup test successful\n' in selenium.page_source

class SuperuserCreationTestCase(LiveServerTestCase):

    def create_superuser_model(self):
        return models.User.objects.create_superuser(email='admin3@admin3.com',password='pickpocket')

    def test_user_creation(self):
        w = self.create_superuser_model()
        self.assertTrue(isinstance(w, models.User))

class StaffCreationTestCase(LiveServerTestCase):

    def create_staff_model(self):
        return models.User.objects.create_staff(email='admin3@admin3.com', password='pickpocket')

    def test_user_creation(self):
        w = self.create_staff_model()
        self.assertTrue(isinstance(w, models.User))

class EmailFailTestCase(LiveServerTestCase):

    def create_staff_model(self):
        return models.User.objects.create_user(email='',password='pickpocket')

    def test_user_creation(self):
        try:
            w = self.create_staff_model()
        except ValueError as e:
            self.assertEquals(str(e),"Please enter an email")

class StrTestCase(LiveServerTestCase):

    def create_staff_model(self):
        return models.User.objects.create_user(email='admin3@admin3.com', password='pickpocket')

    def test_user_creation(self):
        w = self.create_staff_model()
        self.assertEquals(w.__str__(),w.email)

class IsAdminTestCase(LiveServerTestCase):
    def create_staff_model(self):
        return models.User.objects.create_superuser(email='admin3@admin3.com', password='pickpocket')

    def test_user_creation(self):
        w = self.create_staff_model()
        self.assertEquals(w.is_admin,True)

class IsStaffTestCase(LiveServerTestCase):
    def create_staff_model(self):
        return models.User.objects.create_staff(email='admin3@admin3.com', password='pickpocket')

    def test_user_creation(self):
        w = self.create_staff_model()
        self.assertEquals(w.is_staff,True)

class LoginformValidTest(LiveServerTestCase):
    def create_staff_model(self):
        return models.User.objects.create_user(email='admin3@admin3.com', password='pickpocket')

    def test_valid_loginform(self):
        w = self.create_staff_model()
        data = {'email':'admin3@admin3.com','password':'pickpocket'}
        form = forms.LoginForm(data = data)
        self.assertTrue(form.is_valid())

    def test_invalid_loginform(self):
        w = self.create_staff_model()
        data = {'email': 'admin3@admin3.com', 'password': 'picket'}
        try:
            form = forms.LoginForm(data=data)
            self.assertFalse(form.is_valid())
        except ValueError as e:
            self.assertEquals(str(e),"Invalid credentials. User does not exist")



class RegisterformValidTest(TestCase):
    # def create_staff_model(self):
    #     return models.User.objects.create_user(email='admin3@admin3.com', password='pickpocket')

    def test_valid_registerform(self):
        # w = self.create_staff_model()
        data = {
            'first_name': 'test1',
            'last_name': 'user1',
            'oname': 'SKNCOE',
            'bdate': '1989-08-20',
            'email': 'test@test.com',
            'password1': 'adminadmin',
            'password2': 'adminadmin'
        }
        form = forms.RegisterForm(data = data)
        self.assertTrue(form.is_valid())

    def test_invalid_registerform(self):
        # w = self.create_staff_model()
        data = {
            'first_name': 'test',
            'last_name': 'user',
            'oname': 'SKNCOE',
            'bdate': '20-08-1994',
            'email': 'admin2@admin2.com',
            'password1': 'pickpocket',
            'password2': 'pickpocket'
        }
        try:
            form = forms.RegisterForm(data=data)
            self.assertFalse(form.is_valid())
        except ValueError as e2:
            self.assertEquals(str(e2),"Error in form")

    def test_safe_save(self):
        data = {
            'first_name': 'test',
            'last_name': 'user',
            'oname': 'SKNCOE',
            'bdate': '1994-08-07',
            'email': 'admin234@admin2.com',
            'password1': 'pickpocket',
            'password2': 'pickpocket'
        }
        try:
            form = forms.RegisterForm(data=data)
            if form.is_valid():
                self.assertTrue(isinstance(form.save(),models.User))
        except ValueError as e:
            self.assertEquals(str(e), "Error in form")
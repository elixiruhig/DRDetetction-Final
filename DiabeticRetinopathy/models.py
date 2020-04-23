from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
import uuid
from datetime import datetime

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


GENDER_OPTIONS = (
                ('Male','Male'),
                ('Female','Female'),
                )


class UserManager(BaseUserManager):

    def create_user(self,email,password=None):
        if not email:
            raise ValueError("Please enter an email")

        user = self.model(
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password):
        user = self.create_user(email, password=password)
        user.admin = True
        user.staff = True
        user.host = True
        user.save(using=self._db)
        return user

    def create_staff(self,email,password):
        user = self.create_user(email,password=password)
        user.staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False,null=True)
    oname = models.CharField(max_length=255, blank=False, null=True)
    bdate = models.DateField(null=True)
    user_id = models.UUIDField(unique=True, default=uuid.uuid4)
    email = models.EmailField(max_length=255, unique=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_staff(self):
        return self.staff

class Report(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    age = models.PositiveIntegerField(blank=False, null=False)
    gender = models.CharField(max_length=10,null = True, choices=GENDER_OPTIONS)
    date = models.DateTimeField(default=datetime.now())
    photo = models.ImageField(upload_to='fundus_images',null=True)

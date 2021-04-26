from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class MyUserManager(BaseUserManager):
    def create_user(self, email, name, lastname, password=None):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(email=self.normalize_email(
            email), name=name, lastname=lastname)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, lastname, password=None):
        user = self.create_user(email=email, name=name,
                                lastname=lastname, password=password)
        user.is_admin = True
        user.save(using=self._db)

        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'lastname']

    def get_full_name(self):
        return '{} {}'.format(self.name, self.lastname)

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

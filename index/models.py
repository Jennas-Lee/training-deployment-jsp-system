from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, number, name, password=None, repository=None, is_active=0):
        user = self.model(
            number=number,
            name=name,
            repository=repository,
            is_active=is_active
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, number, name, password):
        user = self.create_user(
            number,
            name,
            password,
            None,
            1
        )

        user.is_admin = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    number = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=11)
    repository = models.URLField(null=True, blank=True)
    is_active = models.SmallIntegerField(default=0)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'number'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.number

    def has_perm(self, permission, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

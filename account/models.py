from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

class AccountManager(BaseUserManager):
    def create_user(self, email, username, first_name,
                    last_name, phone, address, license_number,
                    password=None, ):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')
        if not first_name or not last_name or not phone or not address or not license_number:
            raise ValueError('Not all fields are filled')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
            license_number=license_number
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, username, first_name, last_name, phone, address, license_number, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
            license_number=license_number
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name = "email", max_length=60, unique = True)
    username = models.CharField(max_length=60, unique = True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add = True)
    is_active = models.BooleanField(default = False)
    last_login = models.DateTimeField(verbose_name = "last login", auto_now_add = True)
    is_admin = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
    first_name = models.CharField(max_length = 60)
    last_name = models.CharField(max_length = 60)
    phone = models.CharField(max_length=11)
    address = models.TextField(blank=True)
    license_number = models.CharField(max_length=15)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name', 'last_name', 'phone', 'address', 'license_number']

    objects = AccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True










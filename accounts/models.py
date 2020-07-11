import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from django.conf import settings
from datetime import datetime


class UserManager(BaseUserManager):
    def create_user(self, user_name, email, first_name, last_name, date_of_birth, sex, profession, phone_number,
                    password=None):
        if not user_name:
            raise ValueError('Users Must Have an User Name')

        user = self.model(
            user_name=user_name,
            email=email,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            sex=sex,
            profession=profession,
            phone_number=phone_number
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, password):
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.create_user(
            user_name=user_name,
            password=password,
            email='admin@admin.com',
            first_name='admin',
            last_name='admin',
            date_of_birth=datetime.now(),
            sex='M',
            profession='admin',
            phone_number=None,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


def upload_location(instance, filename):
    extension = filename.split('.').pop()
    return f'avatars/{instance.id}.{extension}'


def validate_image(image):
    file_size = image.file.size
    limit_kb = settings.AVATAR_LIMIT_KB
    if file_size > limit_kb * 1024:
        raise ValidationError(f'Max Size of file is {limit_kb} kb')


class User(AbstractBaseUser, PermissionsMixin):
    SEX_CHOICES = (
        ('F', 'Female'),
        ('M', 'Male'),
        ('O', 'Other')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        null=False,
        blank=False,
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    user_name = models.CharField(null=False, blank=False, max_length=25, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    first_name = models.CharField(null=False, blank=False, max_length=25)
    last_name = models.CharField(null=False, blank=False, max_length=25)
    join_date = models.DateTimeField(auto_now_add=True)
    profession = models.CharField(null=False, blank=False, max_length=50)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    phone_number = PhoneNumberField(blank=True, null=True)
    date_of_birth = models.DateField(null=False, blank=False)
    avatar = models.ImageField(upload_to=upload_location, null=True, blank=True, validators=[validate_image])
    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = [first_name, last_name, profession, sex, date_of_birth]

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        return self.user_name

    class Meta:
        db_table = "users"

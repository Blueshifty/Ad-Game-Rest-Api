import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, user_name, email, first_name, last_name, date_of_birth, sex, profession, phone_number, password=None):
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

    def create_superuser(self, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser):
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
    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = []

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        return self.user_name

    class Meta:
        db_table = "users"

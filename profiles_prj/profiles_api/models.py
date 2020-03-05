from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    """
    Database model for manager profiles
    """
    def createUser(self, email, name, password=None):
        """
        Create a new user profile
        """
        if not email:
            raise ValueError('Email is mandatory')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)        
        return user

    def createSuperUser(self, email, name, password):
        """
        Create and save new superuser profile
        """
        user = self.createUser(email, name, password)
        user.is_superuser = True # is_superuser is provided by the PermissionsMixin
        user.is_staff = True
        user.save(using=self._db)        
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """
    Database model for user profile
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    #objects = UserProfileManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def getFullName(self):
        """
        Retrieve fullname of user
        """
        return self.name

    def shortName(self):
        """
        Retrieve short name of user
        """
        return self.name

    def __str__(self):
        """
        String representation of user
        """
        return self.email
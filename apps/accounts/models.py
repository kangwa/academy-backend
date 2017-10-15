from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):

	def create_user(self, email, password=None):
		"""
		Creates and saves a User with the given email and password
		"""

		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(email=self.normalize_email(email))
		user.set_password(password)
		user.save(using=self._db)
		return user


	def create_staffuser(self, email, password):
		"""
		Creates and saves a staff user with the given email and password.
		"""
		user = self.create_user(email, password=password)
		user.staff = True
		user.save(using=self._db)
		return user


	def create_superuser(self, email, password):
		"""
		Creates and saves a superuser with the given email and password.
		"""
		user = self.create_user(email, password=password)
		user.staff = True
		user.admin = True
		user.save(using=self._db)
		return user


class User(AbstractBaseUser):
	email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
	date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
	first_name = models.CharField(_('first name'), max_length=30, blank=True)
	last_name = models.CharField(_('last name'), max_length=30, blank=True)
	active = models.BooleanField(default=True)
	staff = models.BooleanField(default=False)
	admin = models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	objects = UserManager()

	def get_full_name(self):
		# The user is identified by their email address
		return self.email

	def get_short_name(self):
		# The user is identified by their email address
		return self.email

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		# Does the user have a specific permission?
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		# Does the user have permissions to view the app `app_label`?
		# Simplest possible answer: Yes, always
		return True

	@property
	def is_staff(self):
		# is a the user a member of staff?
		return self.staff

	@property
	def is_admin(self):
		# Is the user an admin member?
		return self.admin

	@property
	def is_active(self):
		# Is the user active?
		return self.active






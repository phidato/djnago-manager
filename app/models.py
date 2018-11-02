from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class UserProfile(models.Model):
	user = models.OneToOneField(User, related_name='profile')
	company = models.CharField(max_length=200, blank=True)

	def __unicode__(self):
		return self.user.username

def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        profile = UserProfile(user=user, company='askned')
        profile.save()

post_save.connect(create_profile, sender=User)


class UserPost(models.Model):
	title = models.CharField(max_length=100, blank=True)
	category = models.CharField(max_length=100, blank=True)
	description = models.TextField(blank=True)

	def __unicode__(self):
		return self.title

class EmpData(models.Model):
	name = models.CharField(max_length=100, blank=True)
	designation = models.CharField(max_length=100, blank=True)
	age = models.CharField(max_length=10, blank=True)
	salary = models.CharField(max_length=10, blank=True)
	department = models.CharField(max_length=100, blank=True)
	projectid = models.CharField(max_length=20, blank=True)

	def __unicode__(self):
		return self.name

class Project(models.Model):
	name = models.CharField(max_length=100, blank=True)
	startdate = models.CharField(max_length=100, blank=True)
	enddate = models.CharField(max_length=100, blank=True)

	def __unicode__(self):
		return self.name

class Departments(models.Model):
	name = models.CharField(max_length=100, blank=True)
	head = models.CharField(max_length=100, blank=True)

	def __unicode__(self):
		return self.name

class Designation(models.Model):
	title = models.CharField(max_length=100, blank=True)

	def __unicode__(self):
		return self.title

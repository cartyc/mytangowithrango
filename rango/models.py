from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):

	name = models.CharField(max_length=128, unique=True)
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	# Slug wil turn "this is a string" into "this-is-a-string"
	# This will help give us a clean url
	slug = models.SlugField(unique=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		#READ UP on what super is and how (*args, **kwargs) work
		super(Category, self).save(*args, **kwargs)


	def __unicode__(self):
		return self.name

class Page(models.Model):

	category = models.ForeignKey(Category)
	title = models.CharField(max_length=128)
	url = models.URLField()
	views = models.IntegerField(default=0)

	def __unicode__(self):

		return self.title

class userProfile(models.Model):
	#Links User Profile To User Model
	user = models.OneToOneField(User)

	#Profile Attributes
	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to='profile_images', blank=True)

	def __unicode__(self):

		return self.user.username

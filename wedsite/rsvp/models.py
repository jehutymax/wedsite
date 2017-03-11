from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models import Count
# Create your models here.

class Guest(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
	name = models.CharField(max_length=200, null=True, blank=True)
	address1 = models.CharField(max_length=200, null=True, blank=True)
	address2 = models.CharField(max_length=200, null=True, blank=True)
	city = models.CharField(max_length=100, null=True, blank=True)
	state = models.CharField(max_length=2, null=True, blank=True)
	country = models.CharField(max_length=12, null=True, blank=True)
	zipcode = models.CharField(max_length=12, null=True, blank=True)
	email = models.CharField(max_length=100, null=True, blank=True)
	wedding_code = models.CharField(max_length=4)
	eligible_for_dinner = models.BooleanField(default=False)
	first_visit = models.BooleanField(default=True)
	def __str__(self):
		return u'%s (%s)' % (self.name, self.wedding_code)
	def save(self, *args, **kwargs):
		for var in vars(self):
			if not var.startswith('_'):
				if self.__dict__[var] == '':
					self.__dict__[var] = None
		super(Guest, self).save(*args, **kwargs)	

class Event(models.Model):
	name = models.CharField(max_length=50, null=True)
	caption = models.CharField(max_length=80, null=True)
	venue = models.CharField(max_length=50, null=True)
	date = models.DateTimeField(null=True)
	url = models.CharField(max_length=100, null=True)
	def __str__(self):
		return u'%d: %s (%s)' %  (self.id, self.name, self.venue)

class Person(models.Model):
	guest = models.ForeignKey(Guest)
	name = models.CharField(max_length=100, null=True)
	attending = models.BooleanField(default=False)
	def __str__(self):
		return self.name

class Rsvp(models.Model):
	person = models.ForeignKey(Person)
	event = models.ForeignKey(Event)
	going = models.BooleanField(default=False)
	created = models.DateTimeField(
		default=timezone.now())
	modified = models.DateTimeField(
		auto_now=True)
	def __str__(self):
		return u'%s (%s) %s' % (self.person.name, self.event.name, self.going)

class Interest(models.Model):
	event = models.ForeignKey(Event)
	guest = models.ForeignKey(Guest)
	def __str__(self):
		return u'%s [%s]' % (self.event.name, self.guest.name) 






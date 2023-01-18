from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

class Event(models.Model):
  eventTitle = models.CharField(max_length=100)
  description = models.TextField(max_length=2000)
  date = models.DateField('Event Date')
  evtLocation = models.CharField(max_length=50)
  organizer = models.ForeignKey(User, on_delete=models.CASCADE)
  attendees = models.ManyToManyField(User, related_name="attendees")
  
  def __str__(self):
    return f'{self.eventTitle} ({self.id})'

  def get_absolute_url(self):
        return reverse('detail', kwargs={'event_id': self.id})

class Comment(models.Model):
  comment = models.TextField(max_length=1000)
  event = models.ForeignKey(Event, on_delete=models.CASCADE)
  created_on = models.DateTimeField(auto_now_add=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  class Meta:
    ordering = ['created_on']

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12)

class Photo(models.Model):
    url = models.CharField(max_length=200)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for event_id: {self.event_id} @{self.url}"
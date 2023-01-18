import uuid
import boto3
import os
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Event, Comment, User, Photo
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import CommentForm


# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def events_index(request):
  events = Event.objects.all()
  return render(request, 'events/index.html', {
    'events': events
  })

def events_detail(request, event_id):
  event = Event.objects.get(id=event_id)
  attendees = User.objects.exclude(id__in = event.attendees.all().values_list('id'))
  comments_form = CommentForm()
  return render(request, 'events/detail.html', {
    'event': event,
    'comments_form': comments_form,
    'attendees': attendees
  })

def events_comments(request, event_id):
  form = CommentForm(request.POST)
  if form.is_valid():
    new_comment = form.save(commit=False)
    new_comment.user = request.user
    new_comment.event_id = event_id 
    new_comment.save()
  return redirect('detail', event_id = event_id) 
  

class EventCreate(CreateView):
  model = Event
  fields = ['eventTitle', 'description', 'date', 'evtLocation']
  def form_valid(self, form):
    print(self.request.user)
    form.instance.organizer = User.objects.get(username=self.request.user)
    return super().form_valid(form)

class EventUpdate(UpdateView):
  model = Event
  fields = ['eventTitle', 'description', 'date', 'evtLocation']

class EventDelete(DeleteView):
  model = Event
  success_url = '/events'

def add_photo(request, event_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      bucket = os.environ['S3_BUCKET']
      s3.upload_fileobj(photo_file, bucket, key)
      url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
      Photo.objects.create(url=url, event_id=event_id)
    except Exception as e:
      print('An error occurred uploading file to S3')
      print(e)
  return redirect('detail', event_id=event_id)

class CommentCreate(CreateView):
  model = Comment
  fields = ['__all__']

class CommentUpdate(UpdateView):
  model = Comment
  fields = ['comment']

class CommentDelete(DeleteView):
  model = Comment
  def get_success_url(self):
    print("success")
    return f"/events/{self.object.event.id}"

class AttendeesList(ListView):
    model = User
    fields = '__all__'

def assoc_user(request, event_id, user_id):
    Event.objects.get(id=event_id).attendees.add(user_id)
    return redirect('detail', event_id=event_id)
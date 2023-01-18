from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('events/', views.events_index, name='index'),
  path('events/<int:event_id>/', views.events_detail, name='detail'),
  path('events/create/', views.EventCreate.as_view(), name='events_create'),
  path('events/<int:pk>/update/', views.EventUpdate.as_view(), name='events_update'),
  path('events/<int:pk>/delete/', views.EventDelete.as_view(), name='events_delete'),
  path('events/<int:event_id>/comments/', views.events_comments, name='events_comments'),
  path('events/<int:event_id>/comments/create', views.CommentCreate.as_view(), name='comments_create'),
  path('events/<int:pk>/comments/update/', views.CommentUpdate.as_view(), name='comments_update'),
  path('events/<int:pk>/comments/delete/', views.CommentDelete.as_view(), name='comments_delete'),
  path('cats/<int:event_id>/add_photo/', views.add_photo, name='add_photo'),
  path('events/<int:event_id>/assoc_user/<int:user_id>/', views.assoc_user, name='assoc_user'),
  path('accounts/signup/', views.signup, name='signup'),
  path('events/<int:event_id>/attendees/', views.AttendeesList.as_view(), name='events_attendees'),
]
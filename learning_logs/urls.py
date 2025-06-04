"""Defines URL patterns for learning_logs."""

from django.urls import path

from . import views


app_name = 'learning_logs'
urlpatterns = [
    
    # Home page
    path('', views.index, name='index'),
    # Page that shows all topics.
    path('topics/', views.topics, name='topics'),
    # Detail page for a single topic.
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    # Page for adding new topic.
    path('new_topic/', views.new_topic, name='new_topic'),
    # Page for adding new entry.
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path('public_topics/', views.public_topics, name='public_topics'),
    path('make_public/<int:topic_id>/', views.make_public, name='make_public'),
    path('topics/<int:topic_id>/make_private/', views.make_private, name='make_private'),
    path('search/', views.search_topics, name='search'),
    path('categories/', views.categories, name='categories'),
    path('categories/<int:category_id>/', views.category, name='category'),
    path('new_category/', views.new_category, name='new_category'),
    # User profiles and following
    path('user/<str:username>/', views.user_profile, name='user_profile'),
    path('user/<str:username>/follow/', views.follow_user, name='follow_user'),
    path('following/', views.following_list, name='following_list'),
]
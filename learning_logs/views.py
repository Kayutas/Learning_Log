from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Topic, Entry, Category, Following
from django.contrib import messages

from .forms import TopicForm, EntryForm, CategoryForm

# Create your views here.


def check_topic_owner(topic, request):
    """Check if the topic belongs to the current user."""
    if topic.owner != request.user:
        raise Http404("You do not have permission to view this topic.")


def index(request):
    """The home page for Learning_Log."""
    return render(request, 'learning_logs/index.html')



@login_required
def topics(request):
    """Show all topics."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_id):
    """Show a single topic and all its entries."""
    topic = get_object_or_404(Topic, id=topic_id)

    if not topic.public:
        if not request.user.is_authenticated:
            raise Http404("You must be logged in to view this topic.")
        if topic.owner != request.user:
            raise Http404("You do not have permission to view this topic.")
        
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """Add a new topic"""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            
            
            
           
            return redirect('learning_logs:topics')
        
    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


def public_topics(request):
    """Show all public topics."""
    public_topics = Topic.objects.filter(public=True).order_by('date_added')
    context = {'public_topics': public_topics}
    return render(request, 'learning_logs/public_topics.html', context)


@login_required
def make_public(request, topic_id):
    print("Make public view called")
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic, request)
    topic.public = True
    topic.save()
    return redirect('learning_logs:topic', topic_id=topic_id)


@login_required
def make_private(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic, request)
    topic.public = False
    topic.save()
    return redirect('learning_logs:topic', topic_id=topic_id)


@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic, request)
    
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
        
    # Display a blank or invalid form.
    context = {'topic': topic, 'form' :form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def search_topics(request):
    """Search for topics and entries."""
    query = request.GET.get('q', '')
    if query:
        # Search in both public topics and their entries
        topics = Topic.objects.filter(
            Q(public=True) & 
            (Q(text__icontains=query) | Q(entry__text__icontains=query))
        ).distinct()
    else:
        topics = Topic.objects.filter(public=True)
    
    context = {
        'topics': topics,
        'query': query,
    }
    return render(request, 'learning_logs/search_results.html', context)
        

@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(topic, request)
    
    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
        
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

@login_required
def categories(request):
    """Show all categories and their topics."""
    categories = Category.objects.all().order_by('name')
    for category in categories:
        if request.user.is_authenticated:
            # Show public topics and user's private topics
            category.topics = Topic.objects.filter(
                category=category
            ).filter(
                Q(public=True) | Q(owner=request.user)
            ).order_by('-date_added')
        else:
            # Show only public topics
            category.topics = Topic.objects.filter(
                category=category, public=True
            ).order_by('-date_added')
    
    context = {'categories': categories}
    return render(request, 'learning_logs/categories.html', context)

@login_required
def new_category(request):
    """Add a new category."""
    if request.method != 'POST':
        form = CategoryForm()
    else:
        form = CategoryForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:categories')
            
    context = {'form': form}
    return render(request, 'learning_logs/new_category.html', context)

@login_required
def category(request, category_id):
    """Show a single category and all its topics."""
    category = get_object_or_404(Category, id=category_id)
    if request.user.is_authenticated:
        # Show public topics and user's private topics
        topics = Topic.objects.filter(
            category=category
        ).filter(
            Q(public=True) | Q(owner=request.user)
        ).order_by('-date_added')
    else:
        # Show only public topics
        topics = Topic.objects.filter(
            category=category, public=True
        ).order_by('-date_added')
    
    context = {'category': category, 'topics': topics}
    return render(request, 'learning_logs/category.html', context)

@login_required
def user_profile(request, username):
    """Show user profile and their public topics."""
    user = get_object_or_404(User, username=username)
    topics = Topic.objects.filter(owner=user, public=True).order_by('-date_added')
    is_following = Following.objects.filter(follower=request.user, followed=user).exists() if request.user.is_authenticated else False
    followers_count = Following.objects.filter(followed=user).count()
    following_count = Following.objects.filter(follower=user).count()
    
    context = {
        'profile_user': user,
        'topics': topics,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
    }
    return render(request, 'learning_logs/user_profile.html', context)

@login_required
def follow_user(request, username):
    """Follow or unfollow a user."""
    user_to_follow = get_object_or_404(User, username=username)
    
    if request.user == user_to_follow:
        messages.error(request, "You cannot follow yourself.")
        return redirect('learning_logs:user_profile', username=username)
    
    following = Following.objects.filter(follower=request.user, followed=user_to_follow)
    if following.exists():
        following.delete()
        messages.success(request, f"You have unfollowed {username}")
    else:
        Following.objects.create(follower=request.user, followed=user_to_follow)
        messages.success(request, f"You are now following {username}")
    
    return redirect('learning_logs:user_profile', username=username)

@login_required
def following_list(request):
    """Show list of users the current user is following."""
    following = Following.objects.filter(follower=request.user).select_related('followed')
    context = {'following': following}
    return render(request, 'learning_logs/following_list.html', context)
            
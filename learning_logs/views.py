from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db.models import Q

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

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

            
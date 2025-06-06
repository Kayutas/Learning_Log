from django import forms

from .models import Topic, Entry, Category, Comment


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        labels = {
            'name': 'Category Name',
            'description': 'Description (optional)'
        }


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text', 'category', 'public']
        labels = {
            'text': 'Topic',
            'category': 'Category (optional)',
            'public': 'Make this topic public'
        }
        
        
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text', 'public']
        labels = {'text': '', 'public': 'Make this topic public'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text': 'Comment'}
        widgets = {'text': forms.Textarea(attrs={'rows': 3})}
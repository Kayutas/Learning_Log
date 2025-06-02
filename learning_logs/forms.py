from django import forms

from .models import Topic, Entry


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}
        
        
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text', 'public']
        labels = {'text': '', 'public': 'Make this topic public'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
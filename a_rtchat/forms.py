from django.forms import ModelForm
from .models import GroupMessage
from django import forms

class ChatmessageCreateForm(ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['message']
        widgets = {
            'message' : forms.TextInput(attrs={'placeholder': 'Add message', 'class': 'p-4 text-black', 'autofocus': True, 'maxlength': 400})
        }
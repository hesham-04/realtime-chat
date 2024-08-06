from django.shortcuts import render, get_object_or_404, redirect

from a_rtchat.models import ChatGroup
from .forms import ChatmessageCreateForm


# Create your views here.
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, pk=2)
    chat_messages = chat_group.chat_messages.all().order_by('created_at')[:30]
    form = ChatmessageCreateForm()

    if request.htmx:
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            chatmessage = form.save(commit=False)
            chatmessage.group = chat_group
            chatmessage.author = request.user
            chatmessage.save()
            context = {'message':chatmessage,
                       'user':request.user}
            return render(request, 'a_rtchat/partials/chat_message_p.html', context)

    return render(request, 'a_rtchat/chat.html', {'chat_messages':chat_messages, 'form':form})
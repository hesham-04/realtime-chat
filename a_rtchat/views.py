from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from a_rtchat.models import ChatGroup
from .forms import ChatmessageCreateForm
from .models import GroupMessage


# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import ChatGroup
from .forms import ChatmessageCreateForm
from django.http import Http404

def chat_view(request, chatroom_name='public-chat'):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatmessageCreateForm()

    other_user = None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404()
        for member in chat_group.members.all():
            if member != request.user:
                other_user = member
                break

    if request.htmx:
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            chatmessage = form.save(commit=False)
            chatmessage.group = chat_group
            chatmessage.author = request.user
            chatmessage.save()
            context = {'message': chatmessage,
                       'user': request.user}
            return render(request, 'a_rtchat/partials/chat_message_p.html', context)

    # Include chat_group in the context
    context = {
        'chat_messages': chat_messages,
        'form': form,
        'chatroom_name': chatroom_name,
        'chat_group': chat_group,  # Add this line
        'other_user': other_user,
    }

    return render(request, 'a_rtchat/chat.html', context)







def get_or_create_chatroom(request, username):
    if request.user.username == username:
        return redirect('home')
    other_user = User.objects.get(username=username)
    my_chatrooms = request.user.chat_groups.filter(is_private=True)

    if my_chatrooms.exists():
        for chatroom in my_chatrooms:
            if other_user in chatroom.members.all():
                chatroom = chatroom
                break
            else:
                chatroom = ChatGroup.objects.create(is_private = True)
                chatroom.members.add(request.user, other_user)

    else:
        chatroom = ChatGroup.objects.create(is_private = True)
        chatroom.members.add(request.user, other_user)

    return redirect('chatroom', chatroom.group_name)



def chat_file_upload(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)

    if request.htmx and request.FILES:
        print('IF REQUEST HTMX AND REQUEST FILES')
        file = request.FILES['file']
        message = GroupMessage.objects.create(
            group = chat_group,
            author = request.user,
            file = file
        )

        channel_layer = get_channel_layer()

        event = {
                'type': 'message_handler',
                'message': message.id
            }

        async_to_sync(channel_layer.group_send)(
            chatroom_name,event
        )
    return HttpResponse()

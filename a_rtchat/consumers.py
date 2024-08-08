import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from a_rtchat.models import *


class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        print(f"CONSUMER.PY: Connected user: {self.user}")
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        try:
            self.chatroom = get_object_or_404(ChatGroup, group_name=self.chatroom_name)
        except ChatGroup.DoesNotExist:
            self.close()
            return

        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name, self.channel_name
        )

        #ADD AND UPDATE ONLINE USERS # For the online now feature
        if self.user not in self.chatroom.users_online.all():
            self.chatroom.users_online.add(self.user)
            self.update_online_count()
            print(f"Added {self.user} to online list")


        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name, self.channel_name
        )

        if self.user in self.chatroom.users_online.all():
            self.chatroom.users_online.remove(self.user)
            self.update_online_count()
            print(f"Removed {self.user} from online list")

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['message']


        message = GroupMessage.objects.create(
            message = body,
            author = self.user,
            group = self.chatroom
        )

        event = {
            'type': 'message_handler',
            'message': message.id
        }


        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )

    def message_handler(self, event):
        message_id = event['message']
        message = GroupMessage.objects.get(id=message_id)
        context = {
            'message': message,
            'user': self.user
        }
        html = render_to_string('a_rtchat/partials/chat_message_p.html', context)
        self.send(text_data=html)

    def update_online_count(self):
        online_count = self.chatroom.users_online.count() - 1
        event = {
            'type': 'online_count_handler',
            'online_count': online_count
        }
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event)
        print(f'UPDATE METHOD CALLED: {online_count}')


    def online_count_handler(self, event):
        print(f'Online count: {event["online_count"]}')
        online_count = event['online_count']
        html = render_to_string('a_rtchat/partials/online_count.html', {'online_count': online_count})
        self.send(text_data=html)
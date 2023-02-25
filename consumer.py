import configparser
import json

from telethon import TelegramClient, sync
from telethon.tl.functions.channels import GetFullChannelRequest, GetChannelsRequest
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (PeerChannel)
from telethon.errors import SessionPasswordNeededError

def start_client():
    # Reading Configs
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Setting configuration values
    api_id = config['Telegram']['api_id']
    api_hash = config['Telegram']['api_hash']

    api_id = int(api_id)
    api_hash = str(api_hash)

    phone = config['Telegram']['phone']
    username = config['Telegram']['username']
    BOT_TOKEN = config['Telegram']['token']

    print("starting client")
    # Create the client and connect
    client = TelegramClient(username, api_id, api_hash)
    client.start()
    #client.start(bot_token=BOT_TOKEN)

    if not client.is_user_authorized():
        client.send_code_request(phone)
        try:
            client.sign_in(phone, config['Telegram']['phone'])
        except SessionPasswordNeededError:
            client.sign_in(password=input('Password: '))

    print("Client Created")
    return client

def send_message(channel):
    print(channel.stringify())

    res = client.send_message(entity=channel,message="hola soy tu admirador secreto")
    print(res)

    full_request = client(GetFullChannelRequest(channel))
    print('fullcha', full_request)
    print('fullcha', full_request.full_chat)

    for message in client.iter_messages(full_request.full_chat):
        print(message.id, message.text)

def to_music(message):
    if hasattr(message,"media") and message.media is not None and hasattr(message.media.webpage, "title"):
        #todo clean title from [xx] or any other unnecessary data
        return message.media.webpage.title

    #todo leave only spotify filtering out simple messages
    return message.message


def read_messages(client):
    #print(client.get_me().stringify())

    #entity = 'pipocol'
    entity = 'lhincapie0'
    #entity = -1896526550
    #entity = 'pipoplaylistbuilder_bot'
    #entity = 'pipomusic'

    channel_music_id = -1001896526550
    #channel_music_id = 'https://t.me/+Vr-EUpcVnzM2Y2Jh'
    #my_channel = client.get_entity(channel_music_id)
    #print('channel', my_channel)

    result = client(GetChannelsRequest(id=[channel_music_id]))
    channel = result.chats[0]

    offset_id = 0
    limit = 100
    all_messages = []
    total_messages = 0
    total_count_limit = 0

    while True:
        print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
        history = client(GetHistoryRequest(
            peer=channel,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            all_messages.append(to_music(message))
        offset_id = messages[len(messages) - 1].id
        total_messages = len(all_messages)
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break

    print("messages:", all_messages)
    return all_messages

client = start_client()
messages = read_messages(client)
#todo clean none and other invalid inputs
#todo search music in spotify
#todo add music to playlist

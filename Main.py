import discord
import asyncio
from support import log, look_up_dict

logger = log('discord', 'discord.log')

client = discord.Client()
vocab = None


@client.event
async def on_ready():
    global vocab
    server = client.get_server(id='299286624834158603')
    vocab = discord.utils.get(server.channels, name='vocabulary')


@client.event
async def on_message(message):
    print(vocab)
    if message.content.startswith('!dic'):
        words = message.content.split()[1:]
        for word in words:
            post = get_meaning(word)
            await client.send_message(vocab, post)
            await client.delete_message(message)


def get_meaning(word):
    return look_up_dict(word)


if __name__ == '__main__':
    client.run(token)

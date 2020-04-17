import os
import discord

client = discord.Client()

@client.event
async def on_ready():
    print('Ready!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await message.channel.send(message.content)

if __name__ == '__main__':
    token = os.environ['TOKEN']
    client.run(token)

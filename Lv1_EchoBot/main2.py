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

    await echo(message)

async def echo(message):
    msg = message.content
    uid = message.author.id

    await message.channel.send(f'<@!{uid}> 說：「{msg}」')

if __name__ == '__main__':
    token = os.getenv('TOKEN')
    client.run(token)

import os
import discord

class HelloClient(discord.Client):
    async def on_ready(self):
        print('Ready!')

    async def on_message(self, msg):
        if msg.author == self.user:
            return

if __name__ == '__main__':
    token = os.environ['TOKEN']
    HelloClient().run(token)

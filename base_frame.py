import os
import discord
import subprocess as sp

class HelloClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} | Ready')

    async def on_message(self, msg):
        if msg.author == self.user:
            return

if __name__ == '__main__':
    token = os.getenv('TOKEN')
    HelloClient().run(token)

import os
import random
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

class Meow:
    def __init__(self):
        dn = os.path.dirname(__file__)
        dn = os.path.join(dn, 'imgs')
        imgs = os.listdir(dn)
        self.imgs = [os.path.join(dn, path) for path in imgs]

    def get(self):
        return random.choice(self.imgs)

m = Meow()

@bot.command(name='召喚貓貓')
async def meow(ctx):
    uid = ctx.author.id
    await ctx.send(f'<@{uid}> 貓貓來囉 :heart:', file=discord.File(m.get()))

if __name__ == '__main__':
    token = os.environ['TOKEN']
    bot.run(token)

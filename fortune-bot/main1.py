import os
import random
import fortune
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.command(aliases=['抽籤'])
async def draw(ctx):
    fortune = ['大吉', '吉', '小吉', '小凶', '凶', '大凶']
    rtn = random.choice(fortune)

    await ctx.channel.send(rtn)

if __name__ == '__main__':
    token = os.environ['TOKEN']
    bot.run(token)

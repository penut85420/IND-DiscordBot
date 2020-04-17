import os
import random
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.command(aliases=['抽籤'])
async def draw(ctx):
    fortune = ['大吉', '吉', '小吉', '小凶', '凶', '大凶']
    prob = [4, 6, 4, 3, 2, 1]

    rtn = random.choices(fortune, weights=prob)[0]
    uid = ctx.author.id
    rtn = f'<@{uid}> 你抽到 「{rtn}」 :crystal_ball:'

    await ctx.channel.send(rtn)

if __name__ == '__main__':
    token = os.environ['TOKEN']
    bot.run(token)

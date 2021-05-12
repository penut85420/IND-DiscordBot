# Fortune Bot
+ 透過指令 `!抽籤` 來從大吉、吉、小吉、小凶、凶和大凶之中抽一個。
    ![](https://i.imgur.com/H6YVNCE.png)
+ 使用 `discord.ext` 來建立簡易機器人。
    ```python=
    import os
    import random
    import fortune
    from discord.ext import commands

    bot = commands.Bot(command_prefix='!')

    @bot.command()
    async def draw(ctx):
        fortune = ['大吉', '吉', '小吉', '小凶', '凶', '大凶']
        rtn = random.choice(fortune)

        await ctx.channel.send(rtn)
    ```
+ 如果太常抽出不好的籤，使用者容易沮喪，所以我們需要對籤的機率做一點調整。
    ```python=10
    fortune = ['大吉', '吉', '小吉', '小凶', '凶', '大凶']
    prob = [4, 6, 4, 3, 2, 1]

    rtn = random.choices(fortune, weights=prob)[0]
    await ctx.channel.send(rtn)
    ```
+ [完整程式碼](https://git.io/Jffh6)

## Reference
+ [Python - random.choice](https://tinyurl.com/pg6m23g)
+ [discord.py - discord.ext.Commands](https://tinyurl.com/sfj7522)

import os
import random
import discord

class GuessNumber(discord.Client):
    async def on_ready(self):
        self.guessing = set()
        print(f'{self.user} | Ready!')

    async def on_message(self, ctx: discord.Message):
        if ctx.author == self.user:
            return

        if ctx.content == '!bye':
            await self.logout()
            await self.close()
        elif ctx.content == '!猜數字':
            await self.guessing_process(ctx)

    async def guessing_process(self, ctx: discord.Message):
        if ctx.channel in self.guessing:
            await ctx.channel.send(f'{ctx.author.mention} 你們已經在猜數字了！')
            return

        self.guessing.add(ctx.channel)
        await ctx.channel.send(f'{ctx.channel.mention} 的猜數字遊戲開始囉！')

        await self.guess_number(ctx)

        self.guessing.remove(ctx.channel)
        await ctx.channel.send(f'{ctx.channel.mention} 的猜數字遊戲結束了！')

    async def guess_number(self, ctx: discord.Message):
        lower, upper, guess = 1, 99, -1
        number = random.randint(lower, upper)

        send = ctx.channel.send
        def check(m: discord.Message):
            return m.channel == ctx.channel and m.author != self.user

        prefix = ''
        while guess != number:
            await send(f'{prefix}請在 {lower} 到 {upper} 之間猜一個數字')
            msg = await self.wait_for('message', check=check)
            try:
                guess = int(msg.content)
            except:
                await send(f'{msg.author.mention} 請輸入整數！')
            if guess > lower and guess < number:
                prefix, lower = '太小囉！', guess
            elif guess < upper and guess > number:
                prefix, upper = '太大囉！', guess

        await send(f'恭喜 {msg.author.mention} 猜對了！')

if __name__ == '__main__':
    token = os.getenv('TOKEN')
    GuessNumber().run(token)

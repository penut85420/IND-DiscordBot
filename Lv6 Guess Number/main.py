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
            if ctx.channel in self.guessing:
                await ctx.channel.send(f'{ctx.author.mention} 你們已經在猜數字了！')
                return
            self.guessing.add(ctx.channel)
            await self.guess_number(ctx)
            self.guessing.remove(ctx.channel)

    async def guess_number(self, ctx: discord.Message):
        lower = 0
        upper = 100
        number = random.randint(lower, upper)
        guess = -1
        send = ctx.channel.send
        def check(m: discord.Message):
            return m.channel == ctx.channel and m.author != self.user

        while guess != number:
            await send(f'請在 {lower} 到 {upper} 之間猜一個數字')
            msg = await self.wait_for('message', check=check)
            try:
                guess = int(msg.content)
            except:
                await send(f'{msg.author.mention} 請輸入整數！')
            if guess > lower and guess < number:
                lower = guess
            elif guess < upper and guess > number:
                upper = guess

        await send(f'恭喜 {msg.author.mention} 猜對了！')

if __name__ == '__main__':
    token = os.environ['TOKEN']
    GuessNumber().run(token)

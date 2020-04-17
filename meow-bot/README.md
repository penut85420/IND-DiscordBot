# MeowMeow Bot
+ 用 Discord Bot 發送貓貓照片！
    ![](https://i.imgur.com/9w1tVjz.png)
+ 只要能取得檔案路徑，就可以使用 `discord.File` 來發送圖片檔案。
+ 善用 `os` 來解決檔案路徑的問題：
    ```python=8
    class Meow:
        def __init__(self):
            dn = os.path.dirname(__file__)
            dn = os.path.join(dn, 'imgs')
            imgs = os.listdir(dn)
            self.imgs = [os.path.join(dn, path) for path in imgs]

        def get(self):
            return random.choice(self.imgs)

    m = Meow()
    ```
+ 發送圖片的指令：
    ```python=20
    @bot.command(name='召喚貓貓')
    async def meow(ctx):
        uid = ctx.author.id
        await ctx.send(
            f'<@{uid}> 貓貓來囉 :heart:',
            file=discord.File(m.get())
        )
    ```

## Reference
+ [Python - os.path](https://tinyurl.com/lj4qkau)
    + [os.path.dirname](https://tinyurl.com/ph4e432)
    + [os.path.join](https://tinyurl.com/ormjqed)
+ [Python - os.listdir](https://tinyurl.com/olcm7l6)
+ [discord.py - discord.File](https://tinyurl.com/yb24g4ny)
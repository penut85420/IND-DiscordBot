import os
import re
import random
import asyncio
import discord
from collections import namedtuple

class Player:
    def __init__(self):
        self.money = 0
        self.diamonds = 0
        self.total = [0, 0, 0]

class DrawGameBot(discord.Client):
    def __init__(self, *args, **kwargs):
        self.data = {}
        self.prob = [100, 10, 1]
        self.name = ['4 星', '5 星', '6 星']
        self.money = list(range(1000))
        self.money_prob = list(range(500)) + list(reversed(range(500)))
        self.card = {
            '4 星': [
                '熱血的鵝卵石', '善良的芭樂', '活潑的香蕉皮', '憤怒的葡萄籽',
                '柔軟的衛生紙', '古老的舊皮夾', '快樂的垃圾袋', '旋轉的捲線器',
                '暴力的束口袋', '溫柔的針線包', '殘忍的便條紙', '無情的撲克牌',
            ],
            '5 星': [
                '世界救贖之逗貓棒', '毀天滅地之手機架', '唯我獨尊之魔術方塊',
                '大慈大悲之隨身碟', '電競棉花棒'
            ],
            '6 星': [
                '可愛小蘿莉', '豐滿大歐派', '傳說級醫療口罩', '神之消毒酒精'
            ],
        }
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print('Ready!')

    async def on_message(self, msg):
        if not self.is_handleable(msg):
            return

        await self.handle_commands(msg)

    def is_handleable(self, msg):
        if msg.author == self.user:
            return False
        if not msg.content.startswith('!'):
            return False

        return True

    async def handle_commands(self, msg):
        cmd, args = self.process_command(msg.content)
        cmd_fn = f'cmd_{cmd}'
        cmd_fn = getattr(self, cmd_fn, None)

        if cmd_fn is not None:
            await cmd_fn(msg, args)

    def process_command(self, cmd):
        cmd = cmd.strip()

        if not cmd.startswith('!'):
            return None

        cmd = cmd[1:]
        cmd = re.split('[\s]+', cmd)

        return cmd[0], cmd[1:]

    async def cmd_help(self, msg, args):
        await self.send_msg(msg, (
            '【蝦米碗糕抽卡人生】\n\n'
            '`!help` 顯示本說明訊息\n'
            '`!status` 可以檢視玩家資料\n'
            '`!earn` 可以打工賺錢\n'
            '`!buy` 可以購買鑽石\n'
            '`!draw` 可以抽卡\n'
        ))

    async def cmd_earn(self, msg, args):
        try:
            n = int(args[0])
        except:
            n = 1
        
        _send = msg.channel.send
        if n > 1:
            await _send('打工超過一次的結果將會以私人訊息傳送！')
            _send = msg.author.send

        for _ in range(n):
            uid, player = self.get_player(msg)

            money = random.choices(self.money, weights=self.money_prob)[0]
            player.money += money
            self.data[uid] = player

            rtn = f'{self.tag_name(msg)} 打工賺錢，獲得了 {money} 元！'

            await _send(rtn)
            await asyncio.sleep(1)

    async def cmd_status(self, msg, args):
        uid, player = self.get_player(msg)

        rtn = (
            f'【{self.tag_name(msg)} 的個人資料】\n\n'
            f'金錢：{player.money}\n'
            f'鑽石：{player.diamonds}\n'
            f'四星：{player.total[0]}\n'
            f'五星：{player.total[1]}\n'
            f'六星：{player.total[2]}\n'
        )

        await self.send_msg(msg, rtn)

    async def cmd_buy(self, msg, args):
        if not args:
            rtn = (
                '!buy [要購買的鑽石數量]\n'
                '請輸入要購買的數量\n'
                '購買 1 顆鑽石要 50 塊錢\n'
                '購買 10 顆鑽石只要 400 塊錢\n'
            )
            await self.send_msg(msg, rtn)
            return

        try:
            num = int(args[0])
        except:
            await self.send_msg(msg, '請輸入整數數量')
            return

        ten = num // 10
        one = num % 10
        total = ten * 400 + one * 50

        uid, player = self.get_player(msg)
        if player.money < total:
            rtn = f'{self.tag_name(msg)} 的錢不夠，還需要 {total - player.money} 塊錢！'
            await self.send_msg(msg, rtn)
            return

        player.money -= total
        player.diamonds += num
        self.data[uid] = player

        rtn = f'{self.tag_name(msg)} 花費了 {total} 塊錢購買了 {num} 顆鑽石！'
        await self.send_msg(msg, rtn)

    async def cmd_draw(self, msg, args):
        if not args:
            rtn = (
                '!draw [抽的數量]\n'
                '請輸入要抽的數量\n'
                '抽 1 次要 5 顆鑽石\n'
                '抽 10 次要 50 顆鑽石\n'
                '十抽沒有保底，ㄏㄏ'
            )
            await self.send_msg(msg, rtn)
            return

        try:
            num = int(args[0])
        except:
            await self.send_msg(msg, '請輸入整數數量')
            return

        total = num * 5
        uid, player = self.get_player(msg)
        if player.diamonds < total:
            rtn = f'{self.tag_name(msg)} 的鑽石不夠，還需要 {total - player.diamonds} 顆鑽石！'
            await self.send_msg(msg, rtn)
            return

        async def send(msg, rtn):
            await msg.channel.send(rtn)
        if num > 5:
            await send(msg, '超過五張的抽卡結果將會改成私人訊息！')
            async def send(msg, rtn):
                await msg.author.send(rtn)

        player.diamonds -= total
        await send(msg, f'{self.tag_name(msg)} 抽到了：\n')

        r = [0, 0, 0]
        for i in range(num):
            name = random.choices(self.name, self.prob)[0]
            card = random.choice(self.card[name])
            idx = self.name.index(name)
            r[idx] += 1
            player.total[idx] += 1
            result = f'【{name}】 {card}'
            if '4' not in result:
                result = f'**{result}**'
            if '6' in result:
                result = f'__{result}__'
            await send(msg, result)
            await asyncio.sleep(1)

        self.data[uid] = player
        rtn = f'{self.tag_name(msg)} 抽完了，總共有 {r[0]} 張 4 星，{r[1]} 張 5 星，{r[2]} 張 6 星！'
        await self.send_msg(msg, rtn)

    async def cmd_cheat(self, msg, args):
        uid, player = self.get_player(msg)
        player.money += 100000
        player.diamonds += 100000
        self.data[uid] = player

        rtn = f'{self.tag_name(msg)} 發動作弊之力，獲得了 100000 的金錢與鑽石！'
        await self.send_msg(msg, rtn)

    async def cmd_bye(self, msg, args):
        await msg.channel.send('Bye!')
        await self.logout()
        await self.close()

    async def send_msg(self, msg, rtn):
        await msg.channel.send(rtn)

    def get_player(self, msg):
        uid = msg.author.id
        player = self.data.get(uid, Player())

        return uid, player

    def tag_name(self, msg):
        return f'**{msg.author.display_name}**'

if __name__ == '__main__':
    token = os.environ['TOKEN']
    DrawGameBot().run(token)

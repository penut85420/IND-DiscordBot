import re
import os
import discord
import pickle as pk
from collections import namedtuple

Config = namedtuple('Config', ['channel', 'right_role', 'wrong_role', 'fmt'])

class HelloClient(discord.Client):
    def __init__(self, *args, **kwargs):
        self.registered_channels = {}
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print('Ready!')

    async def on_message(self, msg):
        if msg.author == self.user:
            return

        if not msg.content.startswith('!'):
            return

        admin = [role.permissions.administrator for role in msg.author.roles]
        admin = any(admin)

        if not admin:
            return

        await self.handle_commands(msg)

    async def handle_commands(self, msg):
        cmd, args = process_command(msg.content)
        cmd_fn = f'cmd_{cmd}'
        cmd_fn = getattr(self, cmd_fn, None)

        if cmd_fn is not None:
            await cmd_fn(msg, args)

    async def cmd_register(self, msg, args):
        if len(args) < 4:
            await msg.channel.send('參數數量不正確：!register [公告頻道] [暱稱正確的身分組] [暱稱不正確的身分組] [暱稱格式]')
            return

        channel_id = get_id(args[0])
        right_role = get_id(args[1])
        wrong_role = get_id(args[2])

        def attr_search(attr, target):
            return lambda x: getattr(x, attr) == target

        async def get_target(target_id, target_list, org_arg, target_type):
            target = discord.utils.find(attr_search('id', target_id), target_list)

            if target is None:
                target = discord.utils.find(attr_search('name', target_id), target_list)

            if target is None:
                await msg.channel.send(f'{target_type}不存在：{org_arg}')
                return None

            return target

        channel = await get_target(channel_id, msg.guild.channels, args[0], '頻道')
        right_role = await get_target(right_role, msg.guild.roles, args[1], '角色')
        wrong_role = await get_target(wrong_role, msg.guild.roles, args[2], '角色')

        if not all([channel, right_role, wrong_role]):
            return

        if not isinstance(channel, discord.channel.TextChannel):
            await msg.channel.send(f'「{channel.name}」不是個文字頻道')
            return

        await channel.send((
            f'設定成功！從今開始，'
            f'暱稱格式正確的人會成為 <@&{right_role.id}>，'
            f'格式錯誤的人將會變成 <@&{wrong_role.id}>，'
            f'並且會把相關訊息放在 <#{channel.id}>。'
        ))

        self.registered_channels[channel.guild.id] = Config(
            channel=channel,
            right_role=right_role,
            wrong_role=wrong_role,
            fmt=' '.join(args[3:])
        )

        print(self.registered_channels)

    async def cmd_clear(self, msg, args):
        limit = int(args[0])
        i = 1
        async for m in msg.channel.history(limit=limit):
            print(f'{i}/{limit}', end='\r')
            await m.delete()
            i += 1

    async def cmd_bye(self, msg, args):
        await self.logout()
        await self.close()

    async def on_member_update(self, before, after):
        if after.guild.id not in self.registered_channels:
            return

        config = self.registered_channels[after.guild.id]

        def _valid_nick(name):
            return valid_nick(name, config.fmt)

        valid_before = _valid_nick(before.display_name)
        valid_after = _valid_nick(after.display_name)

        role_before = config.right_role if valid_before else config.wrong_role
        role_after = config.right_role if valid_after else config.wrong_role

        if valid_before ^ valid_after:
            await after.remove_roles(role_before)
            await after.add_roles(role_after)
            await config.channel.send(f'<@!{after.id}> 變成 {role_after} 了！')

def valid_nick(s, fmt):
    if s is None:
        return False

    if re.match(fmt, s):
        return True

    return False

def process_command(cmd):
    cmd = cmd.strip()

    if not cmd.startswith('!'):
        return None

    cmd = cmd[1:]
    cmd = re.split('[\s]+', cmd)

    return cmd[0], cmd[1:]

def get_id(s):
    m = re.search(r'\<[\#\!\@\&]+([^\>]+)\>', s)
    if not m:
        return s
    return int(m.group(1))

def load_pkl(path):
    with open(path, 'rb') as pkl:
        return pk.load(pkl)

def dump_pkl(obj, path):
    with open(path, 'wb') as pkl:
        pk.dump(obj, pkl)

if __name__ == '__main__':
    token = os.getenv('TOKEN')
    HelloClient().run(token)

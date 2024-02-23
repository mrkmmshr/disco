import discord
import traceback
from discord.ext import commands
from os import getenv
import requests

# LINE Notifyのアクセストークン
LINE_NOTIFY_ACCESS_TOKEN = 'YTrWPR8t1V7203V3Ok90AWcB8d1FgJ0dFVPj030lyxm'

# Discord Botのトークン
DISCORD_BOT_TOKEN = 'MTIxMDU1MDE1MjE3NjIwNTgyNA.GaABcT.eHDrlvgWMY9fh30KkJxDfZjKAZA3aSiAVi1_EA'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.event
async def on_message(message):
    if message.content == 'ping':
        # LINE Notifyに通知
        message = 'pong'
        headers = {'Authorization': f'Bearer {LINE_NOTIFY_ACCESS_TOKEN}'}
        data = {'message': message}
        requests.post('https://notify-api.line.me/api/notify', headers=headers, data=data)


bot.run(DISCORD_BOT_TOKEN)

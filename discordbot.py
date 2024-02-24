import requests
import discord
import traceback
from discord.ext import commands
from os import getenv

# LINE Notifyのアクセストークン
LINE_NOTIFY_ACCESS_TOKEN = 'elAVuc7T0cgDIMTtGJYH0nod7ipgnztlQm4Gb3wR5rv'


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')
    # 送信したいメッセージ
    message = 'Hello, world!'

    # ヘッダーとデータの準備
    headers = {'Authorization': f'Bearer {LINE_NOTIFY_ACCESS_TOKEN}'}
    data = {'message': message}

    # リクエスト送信
    requests.post('https://notify-api.line.me/api/notify', headers=headers, data=data)


token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)

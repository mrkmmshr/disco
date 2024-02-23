import discord
import traceback
from discord.ext import commands
from os import getenv
import requests

# LINE Notifyのアクセストークン
LINE_NOTIFY_ACCESS_TOKEN = 'YTrWPR8t1V7203V3Ok90AWcB8d1FgJ0dFVPj030lyxm'

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
    if message.author.bot:
        return

    # 送信元チャンネルが特定のチャンネル以外の場合、処理をスキップ
    if message.channel.id != CHANNEL_ID:
        return

    # メッセージ内容をLINE Notifyに送信
    headers = {'Authorization': f'Bearer {LINE_NOTIFY_ACCESS_TOKEN}'}
    data = {'message': message.content}
    requests.post('https://notify-api.line.me/api/notify', headers=headers, data=data)


token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)

import discord
import traceback
from discord.ext import commands
from os import getenv
import requests

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
    # LINE Notifyに通知
    message = f'**Discordサーバー:** {ctx.guild.name}\n' \
              f'**チャンネル:** {ctx.channel.name}\n' \
              f'**ユーザー:** {ctx.author.name}({ctx.author.id})\n' \
              f'**コマンド:** /ping'
    headers = {'Authorization': f'Bearer {LINE_NOTIFY_ACCESS_TOKEN}'}
    data = {'message': message}
    requests.post('https://notify-api.line.me/api/notify', headers=headers, data=data)

    await ctx.send('pong')


token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)

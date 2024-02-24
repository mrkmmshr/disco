import discord
import traceback
import requests
from discord.ext import commands
from os import getenv

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

# LINE Notify にメッセージを送る関数
def send_line_notify(message):
    line_token = getenv('LINE_NOTIFY_TOKEN')
    headers = {'Authorization': f'Bearer {line_token}'}
    payload = {'message': message}
    requests.post('https://notify-api.line.me/api/notify', headers=headers, data=payload)

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.event
async def on_message(message):
    if 'スプラ' in message.content:
        send_line_notify(f'Discord に「スプラ」が含まれるメッセージが投稿されました: {message.content}')
    await bot.process_commands(message)

token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)

import discord
import traceback
import requests
from discord.ext import commands
from os import getenv

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

# LINE Notifyのトークンをここに設定
line_notify_token = 'YOUR_LINE_NOTIFY_TOKEN'
line_notify_api = 'https://notify-api.line.me/api/notify'


def send_line_notify(notification_message):
    headers = {
        'Authorization': f'Bearer {line_notify_token}'
    }
    data = {
        'message': f'message: {notification_message}'
    }
    response = requests.post(line_notify_api, headers=headers, data=data)
    return response.status_code


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
    # ボット自身のメッセージは無視する
    if message.author == bot.user:
        return

    # メッセージに「Splatoon」という単語が含まれていたらLINEに通知
    if 'Splatoon' in message.content:
        send_line_notify(f'{message.author} mentioned Splatoon in Discord.')
    
    # コマンド処理を続行
    await bot.process_commands(message)


token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)

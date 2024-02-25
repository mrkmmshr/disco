import discord
import traceback
import aiohttp
from discord.ext import commands
import os

# 環境変数の確認
line_notify_token = os.environ.get('LINE_NOTIFY_TOKEN')
if not line_notify_token:
    raise ValueError("LINE_NOTIFY_TOKEN is not set in environment variables.")

discord_bot_token = os.environ.get('DISCORD_BOT_TOKEN')
if not discord_bot_token:
    raise ValueError("DISCORD_BOT_TOKEN is not set in environment variables.")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)
line_notify_api = 'https://notify-api.line.me/api/notify'

async def send_line_notify(notification_message):
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': f'message: {notification_message}'}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(line_notify_api, headers=headers, data=data) as response:
                if response.status != 200:
                    # ログ出力等のエラーハンドリング
                    print(f"Error: {response.status} - {await response.text()}")
        except Exception as e:
            # ログ出力等のエラーハンドリング
            print(f"Exception during LINE Notify request: {e}")

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

    # メッセージに「通話開始」という単語が含まれていたらLINEに通知
    if '通話開始' in message.content:
        await send_line_notify('Discordで通話が始まりました.')

    # メッセージに「通話終了」という単語が含まれていたらLINEに通知
    if '通話終了' in message.content:
        await send_line_notify('Discordで通話が終わりました.')

    # 他のコマンドも正しく動作するようにする
    await bot.process_commands(message)

bot.run(discord_bot_token)

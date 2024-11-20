import discord
from discord.ext import commands
import os 
import asyncio
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

TOKEN = 'TOKEN'  # Замените на ваш токен
CHANNEL_ID = 1308436301673922590
TAG = '<@&1276905054116384839>'

# Глобальная переменная для хранения последнего отправленного сообщения
last_message = None

# Загружаем cogs
async def load_cogs():
    try:
        await bot.load_extension("cogs.moderation")
        print("Cog успешно загружен!")
    except Exception as e:
        print(f"Ошибка при загрузке cog: {e}")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await load_cogs()
    bot.loop.create_task(send_message())

@bot.event
async def on_member_join(member):
    role_name = "unverify"
    role = discord.utils.get(member.guild.roles, name=role_name)
    if role:
        await member.add_roles(role)
        print(f'Роль {role_name} была выдана пользователю {member.name}')
    else:
        print(f'Роль {role_name} не найдена на сервере')

async def send_message():
    global last_message
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    while True:
        if last_message:
            try:
                await last_message.delete()
            except discord.errors.NotFound:
                pass
        last_message = await channel.send(TAG + '''
**Большая просьба в скором времени пройти верификацию.**  
Наши хелперы с радостью тебе помогут! 😊

Не забудь выполнить все шаги в процессе верификации, чтобы получить доступ ко всем каналам! 🔑
''')
        await asyncio.sleep(3600)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Команда не найдена. Пожалуйста, используйте `!commands` для получения списка команд.")
    else:
        await ctx.send(f"Произошла ошибка: {error}")
        print(f"Произошла ошибка: {error}")

# Запуск бота
bot.run(TOKEN)
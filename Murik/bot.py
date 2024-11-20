import discord
from discord.ext import commands
import os 
import asyncio
from datetime import datetime, timedelta
from discord.ext import tasks


intents = discord.Intents.default()
intents.message_content = True  # Для получения контента сообщений
bot = commands.Bot(command_prefix='!', intents=intents)

# Токен вашего бота
TOKEN = 'Njc4OTI0ODQ1OTU3Nzc1MzYw.GWO2sN.a7kGZS-AQYfEN8PMp9f3nhyWq-cz4XZYnkrBL8'

# Загружаем cogs
try:
    bot.load_extension("cogs.moderation")  # Указываем путь к вашему cogs
    print("Cog успешно загружен!")
except Exception as e:
    print(f"Ошибка при загрузке cog: {e}")
    
# Событие, которое срабатывает, когда новый пользователь присоединяется
@bot.event
async def on_member_join(member):
    # Замените "верификация" на название вашей роли
    role_name = "unverify"
    guild = member.guild
    role = discord.utils.get(guild.roles, name=role_name)

    if role:
        await member.add_roles(role)
        print(f'Роль {role_name} была выдана пользователю {member.name}')
    else:
        print(f'Роль {role_name} не найдена на сервере')

CHANNEL_ID = 1308436301673922590  # Замените на ваш Channel ID
# Тег, который вы хотите использовать (например, для упоминания роли)
TAG = '<@&1276905054116384839>'  # Замените на нужный тег, например, @here или @your_role

intents = discord.Intents.default()
intents.message_content = True  # Для получения контента сообщений (если нужно)

# Создаем экземпляр клиента бота
client = discord.Client(intents=intents)

# Глобальная переменная для хранения последнего отправленного сообщения
last_message = None

# Функция для отправки сообщения каждый час
async def send_message():
    global last_message
    await client.wait_until_ready()  # Ждем, пока бот не подключится
    channel = client.get_channel(CHANNEL_ID)
    while True:
        # Если есть предыдущее сообщение, удаляем его
        if last_message:
            try:
                await last_message.delete()
            except discord.errors.NotFound:
                # Сообщение уже удалено или недоступно
                pass

        # Отправляем новое сообщение
        last_message = await channel.send(TAG + '''
**Большая просьба в скором времени пройти верификацию.**  
Наши хелперы с радостью тебе помогут! 😊

Не забудь выполнить все шаги в процессе верификации, чтобы получить доступ ко всем каналам! 🔑
''')
        
        # Ждем 1 час перед следующей отправкой
        await asyncio.sleep(3600)  # Спим 1 час (3600 секунд)

# Событие, которое срабатывает, когда бот подключается к серверу
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    # Запускаем фоновую задачу по отправке сообщений
    client.loop.create_task(send_message())

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Команда не найдена. Пожалуйста, используйте `!commands` для получения списка команд.")
    else:
        await ctx.send(f"Произошла ошибка: {error}")
        print(f"Произошла ошибка: {error}")# ID канала, в который нужно отправлять сообщения
    
# Запускаем бота
client.run('Njc4OTI0ODQ1OTU3Nzc1MzYw.GWO2sN.a7kGZS-AQYfEN8PMp9f3nhyWq-cz4XZYnkrBL8')

# Запуск бота
bot.run('Njc4OTI0ODQ1OTU3Nzc1MzYw.GWO2sN.a7kGZS-AQYfEN8PMp9f3nhyWq-cz4XZYnkrBL8')



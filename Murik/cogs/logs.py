import discord
from discord.ext import commands
import aiohttp

# Создаем объект intents, чтобы отслеживать события с пользователями
intents = discord.Intents.default()
intents.message_content = True  # Включаем доступ к содержимому сообщений
intents.members = True  # Для получения событий о пользователях (например, кик и бан)

# URL вебхука (поменяйте на свой реальный URL)
WEBHOOK_URL = 'https://discord.com/api/webhooks/1308730968181313566/-zBOALjF1FUtUa5oAiI5l-AumLs9PRsKvQ7hvrNJnmKsax8BEkaCd2NYxZAIWA8Qeh94'

# Событие, которое срабатывает при кике пользователя
@bot.event
async def on_member_remove(member):
    # Получаем журнал аудита, чтобы найти ответственного за кик пользователя
    async for entry in member.guild.audit_logs(action=discord.AuditLogAction.kick, limit=1):
        # Убедимся, что мы нашли запись о кике
        if entry.target == member:
            moderator = entry.user  # Ответственный модератор
            reason = entry.reason  # Причина кика

            # Создаем embed сообщение для кика
            embed = discord.Embed(
                title="Пользователь кикнут",
                description=f"Пользователь **{member.name}#{member.discriminator}** был кикнут с сервера.",
                color=discord.Color.blue()  # Синий цвет для кика
            )
            
            # Устанавливаем аватар пользователя
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            
            # Добавляем информацию о модераторе, причине и сервере
            embed.add_field(name="Ответственный модератор", value=moderator.mention)  # Тег модератора
            embed.add_field(name="Причина", value=reason if reason else "Не указана")
            embed.add_field(name="ID пользователя", value=member.id)
            embed.add_field(name="Сервер", value=member.guild.name)
            embed.timestamp = discord.utils.utcnow()  # Добавляем метку времени

            # Отправляем сообщение через вебхук
            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(WEBHOOK_URL, session=session)
                await webhook.send(embed=embed)  # Отправляем embed

# Запуск бота
bot.run('Njc4OTI0ODQ1OTU3Nzc1MzYw.GWO2sN.a7kGZS-AQYfEN8PMp9f3nhyWq-cz4XZYnkrBL8')

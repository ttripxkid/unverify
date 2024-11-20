import discord
from discord.ext import commands

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Слушатель on_ready для синхронизации слэш-команд с Discord
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user}')
        await self.bot.tree.sync()  # Синхронизация слэш-команд с Discord
        print("Слэш-команды синхронизированы!")

    # Пример слэш-команды
    @discord.app_commands.command(name="hello", description="Приветствие от бота!")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("Привет! Я твой бот.")

    # Пример слэш-команды для пинга
    @discord.app_commands.command(name="ping", description="Проверить задержку бота")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong!")

# Функция для добавления Cog в бота
async def setup(bot):
    await bot.add_cog(Logs(bot))

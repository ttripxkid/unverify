import discord
from discord.ext import commands

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Слэш-команда hello
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()  # Синхронизируем слэш-команды с Discord

    @discord.app_commands.command(name="hello", description="Приветствие от бота!")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("Привет! Я твой бот.")

    # Обычная команда для модераторов
    @commands.command()
    async def modcommands(self, ctx):
        """Команды для модераторов."""
        embed = discord.Embed(
            title="Команды модерирования",
            description="Список команд для администраторов:",
            color=discord.Color.blue()
        )

        embed.add_field(name="!kick @пользователь [причина]", value="Кикнуть пользователя с сервера", inline=False)
        embed.add_field(name="!ban @пользователь [причина]", value="Забанить пользователя на сервере", inline=False)
        embed.add_field(name="!mute @пользователь [время (мин)] [причина]", value="Замутить пользователя на указанное время", inline=False)
        embed.add_field(name="!warn @пользователь [уровень (yellow/orange/red)] [причина]", value="Выдать предупреждение пользователю", inline=False)
        
        await ctx.send(embed=embed)

    # Слэш-команда для проверки пинга
    @discord.app_commands.command(name="ping", description="Проверить задержку бота")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong!")

    # Слэш-команда для информации о пользователе
    @discord.app_commands.command(name="userinfo", description="Информация о пользователе")
    async def userinfo(self, interaction: discord.Interaction, user: discord.Option(discord.User, "Выберите пользователя")):
        await interaction.response.send_message(f"Информация о пользователе: {user}")

# Функция для добавления Cog в бота
async def setup(bot):
    await bot.add_cog(Logs(bot))

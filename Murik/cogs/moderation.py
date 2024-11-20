import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Кикнуть пользователя с сервера."""
        await member.kick(reason=reason)
        await ctx.send(f'Пользователь {member} был кикнут. Причина: {reason if reason else "Не указана."}')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Забанить пользователя на сервере."""
        await member.ban(reason=reason)
        await ctx.send(f'Пользователь {member} был забанен. Причина: {reason if reason else "Не указана."}')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, member: discord.Member, duration: int, *, reason=None):
        """Замутить пользователя на заданное время в минутах."""
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not mute_role:
            mute_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, speak=False, send_messages=False)
        
        await member.add_roles(mute_role, reason=reason)
        await ctx.send(f'Пользователь {member} был замучен на {duration} минут. Причина: {reason if reason else "Не указана."}')
        
        # Снятие мута через указанное время
        await asyncio.sleep(duration * 60) 
        await member.remove_roles(mute_role)
        await ctx.send(f'Пользователь {member} больше не замучен.')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx, member: discord.Member, level: str, *, reason=None):
        """Выдать предупреждение (yellow, orange, red) пользователю."""
        if level not in ['yellow', 'orange', 'red']:
            await ctx.send('Неверный уровень предупреждения. Используйте yellow, orange или red.')
            return
        await ctx.send(f'Пользователю {member} выдано предупреждение уровня {level}. Причина: {reason if reason else "Не указана."}')

    @commands.command()
    async def test(ctx):
        await ctx.send("Команда работает!")
    
# Настроим для бота загрузку cogs
def setup(bot):
    bot.add_cog(Moderation(bot))
    







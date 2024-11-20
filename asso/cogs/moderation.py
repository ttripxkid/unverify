import discord
import asyncio
import aiohttp
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Кикнуть пользователя с сервера."""
        await member.kick(reason=reason)
        await ctx.send(f'🔴 **Пользователь** {member.mention} был **кикнут**.\n'
               f'📝 **Причина:** {reason if reason else "*Не указана*."}')


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Забанить пользователя на сервере."""
        await member.ban(reason=reason)
        await ctx.send(f'🚫 **Пользователь** {member.mention} был **забанен**.\n'
               f'📝 **Причина:** {reason if reason else "*Не указана*."}')


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
        await ctx.send(f'⏳ **Пользователь** {member.mention} был **замучен** на {duration} минут.\n'
               f'📝 **Причина:** {reason if reason else "*Не указана*."}')

        
        # Снятие мута через указанное время
        await asyncio.sleep(duration * 60) 
        await member.remove_roles(mute_role)
        await ctx.send(f'✅ **Пользователь** {member.mention} больше не **замучен**! 🎉')


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx, member: discord.Member, level: str, *, reason=None):
        """Выдать предупреждение (yellow, orange, red) пользователю."""
        if level not in ['yellow', 'orange', 'red']:
            await ctx.send('Неверный уровень предупреждения. Используйте yellow, orange или red.')
            return
        await ctx.send(f'⚠️ **Пользователю** {member.mention} выдано **предупреждение** уровня **{level}**.\n'
               f'📝 **Причина:** {reason if reason else "*Не указана*."}')


    @commands.command()
    async def test(self, ctx):
        """Тестовая команда."""
        await ctx.send("Команда работает!")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
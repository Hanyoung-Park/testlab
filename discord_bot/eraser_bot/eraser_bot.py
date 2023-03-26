import discord
from discord.ext import commands
import asyncio
import datetime

bot = commands.Bot(command_prefix='.')

# 봇이 준비되었을 때 출력되는 메시지
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# 등록된 유저 리스트
registered_users = []

# .set (채널 이름) 명령어
@bot.command()
async def set(ctx, channel_name):
    global channel
    channel = discord.utils.get(ctx.guild.channels, name=channel_name)
    await ctx.send(f'{channel.mention}로 채널이 설정되었습니다.')

# .unset (채널 이름) 명령어
@bot.command()
async def unset(ctx, channel_name):
    global channel
    if channel_name == channel.name:
        channel = None
        await ctx.send(f'{channel_name} 채널이 해제되었습니다.')
    else:
        await ctx.send(f'{channel_name} 채널은 설정된 채널이 아닙니다.')

# .join (비밀번호) 명령어
@bot.command()
async def join(ctx, password):
    global registered_users
    if password == 'blackwind':
        registered_users.append(ctx.author)
        await ctx.send(f'{ctx.author}님, 등록되었습니다.')
    else:
        await ctx.send(f'{ctx.author}님, 비밀번호가 일치하지 않습니다.')

# .clear (숫자) 명령어
@bot.command()
async def clear(ctx, num=1):
    async for message in ctx.channel.history(limit=num+1):
        if message.author == bot.user:
            await message.delete()

# .. 명령어
@bot.command()
async def clearall(ctx):
    global registered_users
    if ctx.author in registered_users:
        await ctx.channel.purge(limit=None)
    else:
        await ctx.send(f'{ctx.author}님, 등록되지 않은 사용자입니다.')

# 1시간마다 채팅방에서 자동으로 메시지 삭제
async def auto_clear():
    while True:
        await asyncio.sleep(3600)
        now = datetime.datetime.now()
        async for message in channel.history(limit=None, after=now-datetime.timedelta(hours=1)):
            if message.author == bot.user:
                continue
            time_difference = now - message.created_at
            if time_difference.total_seconds() >= 3600:
                await message.delete()

# 봇 실행
bot.loop.create_task(auto_clear())
bot.run('TOKEN')

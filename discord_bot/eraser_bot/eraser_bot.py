import discord
from discord.ext import commands
import datetime

bot = commands.Bot(command_prefix='.')

# 변수 초기화
channel_id = None
joined_users = set()

# 채널 설정
@bot.command()
async def set(ctx, channel_name):
    global channel_id
    for channel in ctx.guild.channels:
        if channel.name == channel_name:
            channel_id = channel.id
            await ctx.send(f"{channel_name} 채널이 설정되었습니다.")
            break
    else:
        await ctx.send(f"{channel_name} 채널을 찾을 수 없습니다.")

# 메시지 삭제
@bot.command()
async def(ctx):
    async for message in ctx.channel.history(limit=2):
        if message.author == bot.user:
            await message.delete()
            break

# 모든 메시지 삭제
@bot.command()
async def(ctx):
    if ctx.author.id in joined_users:
        await ctx.channel.purge()
    else:
        await ctx.send("모든 메시지 삭제는 등록된 유저만 가능합니다.")

# 등록된 유저 추가
@bot.command()
async def join(ctx, password):
    global joined_users
    if password == "blackwind":
        joined_users.add(ctx.author.id)
        await ctx.send(f"{ctx.author.mention} 님이 등록되었습니다.")
    else:
        await ctx.send("비밀번호가 올바르지 않습니다.")

# 1시간마다 이전 메시지 삭제
async def delete_old_messages():
    global channel_id
    channel = bot.get_channel(channel_id)
    async for message in channel.history(limit=None):
        if datetime.datetime.utcnow() - message.created_at > datetime.timedelta(hours=1):
            await message.delete()

# 봇 실행
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    while True:
        await delete_old_messages()
        await asyncio.sleep(3600)

# 채널 설정 해제
@bot.command()
async def unset(ctx, channel_name):
    global channel_id
    if channel_id is not None and ctx.guild.get_channel(channel_id).name == channel_name:
        channel_id = None
        await ctx.send(f"{channel_name} 채널 설정이 해제되었습니다.")
    else:
        await ctx.send(f"{channel_name} 채널이 설정되어 있지 않습니다.")

# 봇 토큰 입력
bot.run("BOT_TOKEN")

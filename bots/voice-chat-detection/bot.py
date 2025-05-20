import discord
from discord.ext import commands
from datetime import datetime, timezone
import json
import os
from dotenv import load_dotenv

# 환경 변수 불러오기
load_dotenv()

# 봇 토큰 가져오기
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# 봇 권한 설정
intents = discord.Intents.default()  # 기본 권한 생성
intents.voice_states = True  # 음성 상태 감지 활성화
intents.guilds = True  # 서버(길드) 정보 접근 활성화
intents.members = True  # 멤버 정보 접근 활성화
intents.messages = True  # 메시지 감지 활성화

# 봇 객체 생성 (접두사 : "!")
bot = commands.Bot(command_prefix="!", intents=intents)

# 음성 데이터 저장 파일명 (환경 변수로 지정 가능, 기본값 voice_data.json)
VOICE_DATA_FILE = os.getenv("VOICE_DATA_FILE", "voice_data.json")
user_voice_data = {}  # 사용자별 음성 채널 참가 정보 저장

# 참가 정보 저장
def save_voice_data():
    # user_voice_data를 파일에 저장
    with open(VOICE_DATA_FILE, "w") as f:
        json.dump({str(k): {
            "join_time": v["join_time"].isoformat(),
            "channel_name": v["channel_name"],
            "message_id": v["message_id"]
        } for k, v in user_voice_data.items()}, f)

# 참가 정보 불러오기
def load_voice_data():
    global user_voice_data
    if os.path.exists(VOICE_DATA_FILE):
        with open(VOICE_DATA_FILE, "r") as f:
            data = json.load(f)
            user_voice_data = {
                int(k): {
                    "join_time": datetime.fromisoformat(v["join_time"]),
                    "channel_name": v["channel_name"],
                    "message_id": v.get("message_id")
                } for k, v in data.items()
            }

@bot.event
async def on_ready():
    # 봇 준비되었을 때
    print(f"Logged in as {bot.user}")
    load_voice_data()  # 봇 시작 시 데이터 복원
    for guild in bot.guilds:
        for voice_channel in guild.voice_channels:
            for member in voice_channel.members:
                if not member.bot and member.id not in user_voice_data:
                    join_time = datetime.now(timezone.utc)
                    user_voice_data[member.id] = {
                        "join_time": join_time,
                        "message_id": None,
                        "channel_name": voice_channel.name
                    }
                    save_voice_data()

@bot.event
async def on_disconnect():
    # 봇 연결 끊길 때 데이터 저장
    save_voice_data()

@bot.event
async def on_voice_state_update(member, before, after):
    # 멤버 음성 상태 변경 시
    if member.bot:
        return  # 봇 계정 무시

    # 알림을 보낼 텍스트 채널 이름 지정 (기본값: "voice-room")
    alert_channel_name = os.getenv("VOICE_ALERT_CHANNEL", "voice-room")
    channel = discord.utils.get(member.guild.text_channels, name=alert_channel_name)

    # 음성 채널 참가
    if before.channel is None and after.channel is not None:
        join_time = datetime.now(timezone.utc)
        user_voice_data[member.id] = {
            "join_time": join_time,
            "message_id": None,
            "channel_name": after.channel.name
        }
        save_voice_data()
        
        if channel:
            embed = discord.Embed(
                title="음성 채널 참가 알림",
                description=f"{member.mention}님이 음성 채널에 참가했습니다!",
                color=discord.Color.blue()
            )
            embed.add_field(name="채널", value=f"{after.channel.name}", inline=True)
            embed.add_field(name="참가 시간", value=f"{discord.utils.format_dt(join_time)}", inline=True)
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            message = await channel.send(embed=embed)
            
            user_voice_data[member.id]["message_id"] = message.id
            save_voice_data()

    # 음성 채널 퇴장
    elif before.channel is not None and after.channel is None:
        leave_time = datetime.now(timezone.utc)

        if member.id in user_voice_data:
            join_time = user_voice_data[member.id]["join_time"]
            message_id = user_voice_data[member.id]["message_id"]
            channel_name = user_voice_data[member.id]["channel_name"]
            call_duration = leave_time - join_time
            minutes, seconds = divmod(call_duration.total_seconds(), 60)

            # message_id가 존재하는 경우만 메시지 수정
            if channel and message_id:
                try:
                    message = await channel.fetch_message(message_id)
                    embed = discord.Embed(
                        title="음성 채널 참가 및 종료 알림",
                        description=f"{member.mention}님이 음성 채널에서 나갔습니다.",
                        color=discord.Color.red()
                    )
                    embed.add_field(name="채널", value=f"{channel_name}", inline=True)
                    embed.add_field(name="참가 시간", value=f"{discord.utils.format_dt(join_time)}", inline=True)
                    embed.add_field(name="나간 시간", value=f"{discord.utils.format_dt(leave_time)}", inline=True)
                    embed.add_field(name="통화 시간", value=f"{int(minutes)}분 {int(seconds)}초", inline=False)
                    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
                    await message.edit(embed=embed)
                except discord.NotFound:
                    print(f"메시지를 찾을 수 없음: {message_id}")

            # 사용자 데이터 삭제
            del user_voice_data[member.id]
            save_voice_data()

if not TOKEN:
    raise ValueError("DISCORD_BOT_TOKEN 환경 변수를 설정하세요.")

bot.run(TOKEN)
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="$")

AUDIO_PATH = "./audios/intro.mp3"

# CHANNEL_NAME = "code 'n bake"
CHANNEL_NAME = "flex do milhao"


@bot.command("fdm")
async def intro(ctx):
    voice_channel = discord.utils.get(ctx.guild.channels, name=CHANNEL_NAME)

    vc = await voice_channel.connect()

    audio_source = discord.FFmpegPCMAudio(AUDIO_PATH)
    vc.play(audio_source)

    vc.source = discord.PCMVolumeTransformer(vc.source, volume=0.05)

    while vc.is_playing():
        pass
    await vc.disconnect()


bot.run(TOKEN)

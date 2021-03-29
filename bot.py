import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='$')

AUDIO_PATH = './intro.mp3'


@bot.command('fdm')
async def intro(ctx):
    voice_channel = discord.utils.get(ctx.guild.channels, name="code 'n bake")

    vc = await voice_channel.connect()

    audio_source = discord.FFmpegPCMAudio(AUDIO_PATH)

    vc.play(audio_source)

    while vc.is_playing():
        pass
    await vc.disconnect()


bot.run(TOKEN)

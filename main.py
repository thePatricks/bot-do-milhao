import os
from discord.ext import commands
from dotenv import load_dotenv

from src.controller import Controller

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!")


@bot.command("crime")
async def crime(ctx, *args):
    c = Controller(ctx, *args)
    await c.run()


print("Bot is running!")
bot.run(TOKEN)

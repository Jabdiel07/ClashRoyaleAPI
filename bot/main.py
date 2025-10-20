import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from discord import app_commands
from information_retrieval import get_player_info

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CLASH_API_KEY = os.getenv('CLASH_API_KEY')

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Logged in as {bot.user} | Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Slash command sync error: {e}")

@bot.tree.command(name='ping', description='Check if the bot is alive')
async def ping_slash(interaction: discord.Interaction):
    await interaction.response.send_message('Pong!')

@bot.tree.command(name='user', description='Get Clash Royale player information using their tag id')
@app_commands.describe(user_id='The player tag id (don\'t include the #)')
async def user_command(interaction: discord.Interaction, user_id: str):
    message = get_player_info(user_id)
    await interaction.response.send_message(f'Player Info:\n{message}')
    
if __name__ == '__main__':
    if not DISCORD_TOKEN:
        raise RuntimeError('DISCORD_TOKEN is missing. Put it in your .env file.')
    bot.run(DISCORD_TOKEN)
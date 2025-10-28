import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from discord import app_commands
from information_retrieval import get_player_info
from information_retrieval import get_player_battlelog
from information_retrieval import get_clan_info
from information_retrieval import compare_players

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

@bot.tree.command(name='user_info', description='Get Clash Royale player information using their tag id')
@app_commands.describe(user_id='The player tag id (don\'t include the #)')
async def user_info_command(interaction: discord.Interaction, user_id: str):
    message = get_player_info(user_id)
    await interaction.response.send_message(f'Player Info:\n\n{message}')

@bot.tree.command(name='user_battlelog', description='Get the most recent battle of a player using their tag id')
@app_commands.describe(user_id='The player tag id (don\'t include the #)')
async def user_battlelog_command(interaction: discord.Interaction, user_id: str):
    message = get_player_battlelog(user_id)
    await interaction.response.send_message(f'Recent battle log:\n\n{message}')

@bot.tree.command(name='clan_info', description='Get Clash Royale clan information using the clan tag id')
@app_commands.describe(clan_id='The clan tag id (don\'t include the #)')
async def clan_info_command(interaction: discord.Interaction, clan_id: str):
    message = get_clan_info(clan_id)
    await interaction.response.send_message(f'Clan Info:\n\n{message}')

@bot.tree.command(name='compare', description='Compare two Clash Royale player stats using their tag ids')
@app_commands.describe(user_id1='The first player tag id (don\'t include the #)', user_id2='The second player tag id (don\'t include the #)')
async def compare_command(interaction: discord.Interaction, user_id1: str, user_id2: str):
    message = compare_players(user_id1, user_id2)
    await interaction.response.send_message(f'Player Comparison:\n\n{message}')

if __name__ == '__main__':
    if not DISCORD_TOKEN:
        raise RuntimeError('DISCORD_TOKEN is missing. Put it in your .env file.')
    bot.run(DISCORD_TOKEN)
import discord
import requests
import json
import os
from dotenv import load_dotenv
import math
from datetime import datetime
from discord import Embed

load_dotenv()
def get_card_info(card_name):
    CLASH_API_KEY = os.getenv('CLASH_API_KEY')

    if not CLASH_API_KEY:
        raise RuntimeError('CLASH_API_KEY is missing. Put it in your .env file.')
    
    request = requests.get(f'https://api.clashroyale.com/v1/cards?limit=500', headers={'Accept': 'application/json', 'Authorization': f'Bearer {CLASH_API_KEY}'})

    data = request.json()

    if request.status_code == 200:
        return create_card_information(data, card_name)
    else:
        return f"Error: {data.get('message', 'Unknown error occurred')}"
    
def create_card_information(data, card_name):
    requested_card = card_name.lower()
    items = data.get('items', [])
    chosen = None

    for item in items:
        if item.get('name', '').lower() == requested_card:
            chosen = item
            break

    if not chosen:
        return f"Card '{requested_card}' not found. Please ensure the name is exactly as it appears in the game."
    
    icon_url = chosen.get('iconUrls', {}).get('medium', 'N/A')
    icon_evo_url = chosen.get('iconUrls', {}).get('evolutionMedium', '')
    card_evo = chosen.get('maxEvolutionLevel', 0)

    return {
        'card_name': chosen.get('name', 'N/A'),
        'card_rarity': chosen.get('rarity', 'N/A').capitalize(),
        'elixir_cost': chosen.get('elixirCost', 'N/A'),
        'card_evo': 1 if card_evo > 0 else 0,
        'card_icon': icon_url,
        'card_evo_icon': icon_evo_url
    }

def build_card_embed(card):
    name = card['card_name']
    rarity = card['card_rarity'] or 'N/A'
    elixir = card['elixir_cost']
    evo = card['card_evo']
    icon = card['card_icon']
    evo_icon = card['card_evo_icon']

    if evo == 1:
        embed = discord.Embed(
        title=name,
        description=f"**Rarity:** {rarity}\n**Elixir Cost:** {elixir}\n**Has Evolution:** Yes",
        )
    
    else:
        embed = discord.Embed(
        title=name,
        description=f"**Rarity:** {rarity}\n**Elixir Cost:** {elixir}\n**Has Evolution:** No",
        )

    if icon:
        embed.set_thumbnail(url=icon)
    if evo == 1 and evo_icon:
        embed.set_image(url=evo_icon)

    return embed


def get_card_embed(card_name):
    card_info = get_card_info(card_name)

    if isinstance(card_info, str):
        return card_info

    embed = build_card_embed(card_info)
    return embed
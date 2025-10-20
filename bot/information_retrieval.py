import requests
import json
import os

def get_player_info(player_tag):
    CLASH_API_KEY = os.getenv('CLASH_API_KEY')
    
    if not CLASH_API_KEY:
        raise RuntimeError('CLASH_API_KEY is missing. Put it in your .env file.')

    request = requests.get(f'https://api.clashroyale.com/v1/players/%23{player_tag.upper()}', headers={'Accept': 'application/json', 'authorization': f'Bearer {CLASH_API_KEY}'})

    data = request.json()

    if request.status_code == 200:
        return create_player_info_card(data)
    else:
        return f"Error: {data.get('message', 'Unknown error occurred')}"


def create_player_info_card(data):
    player_name = data.get('name', 'Unknown')
    trophies = data.get('trophies', 'N/A')
    arena = data.get('arena', {}).get('name', 'N/A')

    return f'Player 🫅: {player_name}\nTrophies 🏆: {trophies}\nArena ⚔️: {arena}'


def jprint(data):
   text = json.dumps(data, sort_keys=True, indent=4)
   return text 
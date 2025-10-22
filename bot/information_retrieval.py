import requests
import json
import os
from dotenv import load_dotenv
import math
from datetime import datetime

'''

remove lines 12-17 when finished with this file, it's only here for testing purposes on the functions in this file

'''

load_dotenv()
dummy_CLASH_API_KEY = os.getenv('CLASH_API_KEY')
dummy_player_tag = '8PJGQQQC'
dummy_request = requests.get(f'https://api.clashroyale.com/v1/players/%23{dummy_player_tag.upper()}', headers={'Accept': 'application/json', 'Authorization': f'Bearer {dummy_CLASH_API_KEY}'})
dummy_data = dummy_request.json()
print(dummy_request.status_code)

def get_player_battlelog(player_tag):
    CLASH_API_KEY = os.getenv('CLASH_API_KEY')

    if not CLASH_API_KEY:
        raise RuntimeError('CLASH_API_KEY is missing. Put it in your .env file.')
    
    request = requests.get(f'https://api.clashroyale.com/v1/players/%23{player_tag.upper()}/battlelog', headers={'Accept': 'application/json', 'Authorization': f'Bearer {CLASH_API_KEY}'})

    data = request.json()

    if request.status_code == 200:
        return user_battlelog_card(data)
    else:
        return f"Error: {data.get('message', 'Unknown error occurred')}"
    
def user_battlelog_card(data):
    latest_battle = data[0]
    team = latest_battle.get('team', [])
    opponent = latest_battle.get('opponent', [])

    battle_time = latest_battle.get('battleTime', 'N/A')
    dt = datetime.strptime(battle_time, '%Y%m%dT%H%M%S.%fZ')
    formatted_battle_time = dt.strftime('%B %d, %Y')

    player1 = team[0]
    player_name = player1.get('name', 'Unknown')
    player_tag = player1.get('tag', 'N/A')
    player_crowns = player1.get('crowns', 0)
    player_clan = player1.get('clan', {}).get('name', 'No Clan')
    player_cards_used, player_evos_used, num_evos_used = get_battlelog_cards(player1)


    player2 = opponent[0]
    opponent_name = player2.get('name', 'Unknown')
    opponent_tag = player2.get('tag', 'N/A')
    opponent_crowns = player2.get('crowns', 0)
    opponent_clan = player2.get('clan', {}).get('name', 'No Clan')
    opponent_cards_used, opponent_evos_used, opponent_num_evos_used = get_battlelog_cards(player2)


    return f'Date of Battle 🕒: {formatted_battle_time}\n\nPlayer Name 🫅: {player_name}\nPlayer Tag #️⃣: {player_tag}\nClan 🏰: {player_clan}\nTowers Destroyed 💥: {player_crowns}\nCards Used 🃏: {player_cards_used}\nEvos Used ♦️:({num_evos_used}): {player_evos_used}\n\nOpponent Name 🫅: {opponent_name}\nPlayer Tag #️⃣: {opponent_tag}\nClan 🏰: {opponent_clan}\nTowers Destroyed 💥: {opponent_crowns}\nCards Used 🃏: {opponent_cards_used}\nEvos Used ♦️:({opponent_num_evos_used}): {opponent_evos_used}'

def get_battlelog_cards(user):
    cards_used = []
    evos_used = []
    for card in user.get('cards', []):
        cards_used.append(card.get('name', 'Unknown'))

        if card.get('evolutionLevel'):
            evos_used.append(card.get('name', 'Unknown'))
    
    return ', '.join(cards_used), ', '.join(evos_used), len(evos_used)


def get_player_info(player_tag):
    CLASH_API_KEY = os.getenv('CLASH_API_KEY')
    
    if not CLASH_API_KEY:
        raise RuntimeError('CLASH_API_KEY is missing. Put it in your .env file.')

    request = requests.get(f'https://api.clashroyale.com/v1/players/%23{player_tag.upper()}', headers={'Accept': 'application/json', 'Authorization': f'Bearer {CLASH_API_KEY}'})

    data = request.json()

    if request.status_code == 200:
        return create_player_info_card(data)
    else:
        return f"Error: {data.get('message', 'Unknown error occurred')}"
    
def find_evos(data):
    evolutions = []

    for card in data.get('cards', []):
        if 'evolutionLevel' in card:
            evolutions.append(card.get('name', 'Unknown'))
        
        string = ', '.join(evolutions) if evolutions else 'No evolutions found'
        number_of_evos = len(evolutions)
    
    return string, number_of_evos

def create_player_info_card(data):
    player_name = data.get('name', 'Unknown')
    level = data.get('expLevel', 'N/A')
    trophies = data.get('trophies', 'N/A')
    arena = data.get('arena', {}).get('name', 'N/A')
    best_trophies = data.get('bestTrophies', 'N/A')
    clan = data.get('clan', {}).get('name', 'No Clan')
    evos, num_of_evos = find_evos(data)
    player_wins = data.get('wins', 0)
    player_matches_played = data.get('battleCount', 0)
    player_win_rate = (player_wins / player_matches_played) * 100 if player_matches_played > 0 else 0

    return f'Player 🫅: {player_name}\nPlayer Level 🌟: {level}\nTrophies 🏆: {trophies}\nBest Trophies 🥇: {best_trophies}\nWin Rate 🟢: {math.ceil(player_win_rate)}%\nArena ⚔️: {arena}\nClan 🏰: {clan}\nEvos ({num_of_evos}) ♦️: {evos}'


def get_clan_info(clan_tag):
    CLASH_API_KEY = os.getenv('CLASH_API_KEY')

    if not CLASH_API_KEY:
        raise RuntimeError('CLASH_API_KEY is missing. Put it in your .env file.')
    
    request = requests.get(f'https://api.clashroyale.com/v1/clans/%23{clan_tag.upper()}', headers={'Accept': 'application/json', 'Authorization': f'Bearer {CLASH_API_KEY}'})

    data = request.json()

    if request.status_code == 200:
        return create_clan_info_card(data)
    else:
        return f"Error: {data.get('message', 'Unknown error occurred')}"

def create_clan_info_card(data):
    clan_name = data.get('name', 'Unknown')
    clan_description = data.get('description', 'No description')
    clan_required_trophies = data.get('reqiredTrophies', 0)
    clan_type = data.get('type', 'N/A')
    clan_location = data.get('location', {}).get('name', 'N/A')
    clan_clanWar_trophies = data.get('clanWarTrophies', 0)
    clan_members = data.get('members', 0)
    top_three_players = get_top_three_players_clan(data)

    return f'Clan Name 🏰: {clan_name}\nDescription 📝: {clan_description}\nType 🔰: {clan_type}\nLocation 📍: {clan_location}\nClan War Trophies ⚔️: {clan_clanWar_trophies}\nRequired Trophies 🏆: {clan_required_trophies}\nMembers 👥: {clan_members}\nTop 3 Players 🥇: {top_three_players}'


def get_top_three_players_clan(data):
    members = data.get('memberList', [])
    top_three = [member.get('name', 'Unknown') for member in members[:3]]
    
    return ', '.join(top_three)



def jprint(data):
   text = json.dumps(data, sort_keys=True, indent=4)
   return text 
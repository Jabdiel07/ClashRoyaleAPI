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
    ranks = {0: 'Unranked', 1: 'Bronze', 2: 'Silver', 3: 'Gold', 4: 'Diamond', 5: 'Master I', 6: 'Master II', 7: 'Master III', 6: 'Champion', 9: 'Grand Champion', 10: 'Ultimate Champion'}

    player_name = data.get('name', 'Unknown')
    level = data.get('expLevel', 'N/A')
    trophies = data.get('trophies', 'N/A')
    past_10k_trophies = data.get('progress', {}).get('seasonal-trophy-road-202510', {}).get('trophies', 0)
    past_10k_best_trophies = data.get('progress', {}).get('seasonal-trophy-road-202510', {}).get('bestTrophies', 0)
    arena = data.get('arena', {}).get('name', 'N/A')
    best_trophies = data.get('bestTrophies', 'N/A')
    currentPathOfLegendTrophies = data.get('currentPathOfLegendSeasonResult', {}).get('trophies', 0)
    bestPathOfLegendTrophies = data.get('bestPathOfLegendSeasonResult', {}).get('trophies', 0)
    clan = data.get('clan', {}).get('name', 'No Clan')
    evos, num_of_evos = find_evos(data)
    player_wins = data.get('wins', 0)
    player_matches_played = data.get('battleCount', 0)
    player_win_rate = (player_wins / player_matches_played) * 100 if player_matches_played > 0 else 0

    current_rank_number = data.get('currentPathOfLegendSeasonResult', {}).get('leagueNumber', 'N/A')
    best_rank_number = data.get('bestPathOfLegendSeasonResult', {}).get('leagueNumber', 'N/A')

    current_rank_name = ranks.get(current_rank_number, 'N/A')
    highest_rank_name = ranks.get(best_rank_number, 'N/A')

    seasonal_arena = data.get('progress', {}).get('seasonal-trophy-road-202510', {}).get('arena', {}).get('name', 'N/A')

    if past_10k_trophies > 10000 and past_10k_best_trophies > 15000:
        return f'Player 🫅: {player_name}\nPlayer Level 🌟: {level}\nTrophies 🏆: {past_10k_trophies}\nBest Trophies 🥇: {past_10k_best_trophies}\nCurrent Path Of Legends Trophies 🏅: {currentPathOfLegendTrophies}\nBest Path Of Legends Trophies ⚜️: {bestPathOfLegendTrophies}\nCurrent Rank 🔹: {current_rank_name}\nHighest Rank 🔸: {highest_rank_name}\nSeasonal Arena 🏟️: {seasonal_arena}\nWin Rate 🟢: {math.ceil(player_win_rate)}%\nArena ⚔️: {arena}\nClan 🏰: {clan}\nEvos ({num_of_evos}) ♦️: {evos}'
    elif past_10k_trophies > 10000:
        return f'Player 🫅: {player_name}\nPlayer Level 🌟: {level}\nTrophies 🏆: {past_10k_trophies}\nBest Trophies 🥇: {past_10k_best_trophies}\nWin Rate 🟢: {math.ceil(player_win_rate)}%\nArena ⚔️: {arena}\nClan 🏰: {clan}\nEvos ({num_of_evos}) ♦️: {evos}'
    else:
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


def compare_players(player1_data, player2_data):
    # function to fetch two requests, one for player 1 and one for player 2.
    # this will follow the same structure as the get_player_info function
    # for the retun statament, it will call another function called creare_player_comparison_card
    # this function will follow the same structure as the create_player_info_card function, but it will compare the two players side by side
    pass


def jprint(data):
   text = json.dumps(data, sort_keys=True, indent=4)
   return text 
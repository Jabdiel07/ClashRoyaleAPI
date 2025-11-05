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
    battle_type = latest_battle.get('gameMode', {}).get('name', 'N/A')

    if battle_type != 'TeamVsTeam':
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
    
    else:
        team = latest_battle.get('team', [])
        player1 = team[0]
        player2 = team[1]

        player1_name = player1.get('name', 'Unknown')
        player2_name = player2.get('name', 'Unknown')
        player1_tag = player1.get('tag', 'N/A')
        player2_tag = player2.get('tag', 'N/A')
        player1_clan = player1.get('clan', {}).get('name', 'No Clan')
        player2_clan = player2.get('clan', {}).get('name', 'No Clan')
        player1_cards_used, player1_evos_used, player1_num_evos_used = get_battlelog_cards(player1)
        player2_cards_used, player2_evos_used, player2_num_evos_used = get_battlelog_cards(player2)
        team_crowns = player1.get('crowns', 0)

        opponent = latest_battle.get('opponent', [])

        opponent1 = opponent[0]
        opponent2 = opponent[1]

        opponent1_name = opponent1.get('name', 'Unknown')
        opponent2_name = opponent2.get('name', 'Unknown')
        opponent1_tag = opponent1.get('tag', 'N/A')
        opponent2_tag = opponent2.get('tag', 'N/A')
        opponent1_clan = opponent1.get('clan', {}).get('name', 'No Clan')
        opponent2_clan = opponent2.get('clan', {}).get('name', 'No Clan')
        opponent1_cards_used, opponent1_evos_used, opponent1_num_evos_used = get_battlelog_cards(opponent1)
        opponent2_cards_used, opponent2_evos_used, opponent2_num_evos_used = get_battlelog_cards(opponent2)
        opponent_team_crowns = opponent1.get('crowns', 0)

        battle_time = latest_battle.get('battleTime', 'N/A')
        dt = datetime.strptime(battle_time, '%Y%m%dT%H%M%S.%fZ')
        formatted_battle_time = dt.strftime('%B %d, %Y')

        return f'Date of Battle 🕒: {formatted_battle_time}\n\nTeam:\nPlayer Names 🫅: {player1_name}/{player2_name}\nPlayer Tags #️⃣: {player1_tag}/{player2_tag}\nClans 🏰: {player1_clan}/{player2_clan}\n{player1_name} Cards Used 🃏: {player1_cards_used}\n{player1_name} Evos Used ({player1_num_evos_used}) ♦️: {player1_evos_used}\n{player2_name} Cards Used 🃏: {player2_cards_used}\n{player2_name} Evos Used ({player2_num_evos_used}) ♦️: {player2_evos_used}\nTowers Destroyed 💥: {team_crowns}\n\nOpponent Team:\nOpponent Names 🫅: {opponent1_name}/{opponent2_name}\nOpponent Tags #️⃣: {opponent1_tag}/{opponent2_tag}\nClans 🏰: {opponent1_clan}/{opponent2_clan}\n{opponent1_name} Cards Used 🃏: {opponent1_cards_used}\n{opponent1_name} Evos Used ({opponent1_num_evos_used}) ♦️: {opponent1_evos_used}\n{opponent2_name} Cards Used 🃏: {opponent2_cards_used}\n{opponent2_name} Evos Used ({opponent2_num_evos_used}) ♦️: {opponent2_evos_used}\nTowers Destroyed 💥: {opponent_team_crowns}'

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
    past_10k_trophies = data.get('progress', {}).get('seasonal-trophy-road-202511', {}).get('trophies', 0)
    past_10k_best_trophies = data.get('progress', {}).get('seasonal-trophy-road-202511', {}).get('bestTrophies', 0)
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

    seasonal_arena = data.get('progress', {}).get('seasonal-trophy-road-202511', {}).get('arena', {}).get('name', 'N/A')

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


def compare_players(player_tag_1, player_tag_2):
    CLASH_API_KEY = os.getenv('CLASH_API_KEY')
    
    if not CLASH_API_KEY:
        raise RuntimeError('CLASH_API_KEY is missing. Put it in your .env file.')

    request1 = requests.get(f'https://api.clashroyale.com/v1/players/%23{player_tag_1.upper()}', headers={'Accept': 'application/json', 'Authorization': f'Bearer {CLASH_API_KEY}'})
    request2 = requests.get(f'https://api.clashroyale.com/v1/players/%23{player_tag_2.upper()}', headers={'Accept': 'application/json', 'Authorization': f'Bearer {CLASH_API_KEY}'})

    player1_data = request1.json()
    player2_data = request2.json()

    if request1.status_code == 200 and request2.status_code == 200:
        return create_player_card_comparison(player1_data, player2_data)
    else:
        return f"At least one of the player tags is invalid. Please check and try again."
    

def create_player_card_comparison(player1_data, player2_data):
    ranks = {0: 'Unranked', 1: 'Bronze', 2: 'Silver', 3: 'Gold', 4: 'Diamond', 5: 'Master I', 6: 'Master II', 7: 'Master III', 6: 'Champion', 9: 'Grand Champion', 10: 'Ultimate Champion'}

    player1_name = player1_data.get('name', 'Unknown')
    player1_level = player1_data.get('expLevel', 'N/A')
    player1_trophies = player1_data.get('trophies', 'N/A')
    player1_past_10k_trophies = player1_data.get('progress', {}).get('seasonal-trophy-road-202510', {}).get('trophies', 0)
    player1_past_10k_best_trophies = player1_data.get('progress', {}).get('seasonal-trophy-road-202510', {}).get('bestTrophies', 0)
    player1_arena = player1_data.get('arena', {}).get('name', 'N/A')
    player1_best_trophies = player1_data.get('bestTrophies', 'N/A')
    player1_currentPathOfLegendTrophies = player1_data.get('currentPathOfLegendSeasonResult', {}).get('trophies', 0)
    player1_bestPathOfLegendTrophies = player1_data.get('bestPathOfLegendSeasonResult', {}).get('trophies', 0)
    player1_clan = player1_data.get('clan', {}).get('name', 'No Clan')
    player1_evos, player1_num_of_evos = find_evos(player1_data)
    player1_wins = player1_data.get('wins', 0)
    player1_matches_played = player1_data.get('battleCount', 0)
    player1_win_rate = (player1_wins / player1_matches_played) * 100 if player1_matches_played > 0 else 0

    player1_current_rank_number = player1_data.get('currentPathOfLegendSeasonResult', {}).get('leagueNumber', 'N/A')
    player1_best_rank_number = player1_data.get('bestPathOfLegendSeasonResult', {}).get('leagueNumber', 'N/A')

    player1_current_rank_name = ranks.get(player1_current_rank_number, 'N/A')
    player1_highest_rank_name = ranks.get(player1_best_rank_number, 'N/A')

    player1_seasonal_arena = player1_data.get('progress', {}).get('seasonal-trophy-road-202510', {}).get('arena', {}).get('name', 'N/A')


    player2_name = player2_data.get('name', 'Unknown')
    player2_level = player2_data.get('expLevel', 'N/A')
    player2_trophies = player2_data.get('trophies', 'N/A')
    player2_past_10k_trophies = player2_data.get('progress', {}).get('seasonal-trophy-road-202510', {}).get('trophies', 0)
    player2_past_10k_best_trophies = player2_data.get('progress', {}).get('seasonal-trophy-road-202510', {}).get('bestTrophies', 0)
    player2_arena = player2_data.get('arena', {}).get('name', 'N/A')
    player2_best_trophies = player2_data.get('bestTrophies', 'N/A')
    player2_currentPathOfLegendTrophies = player2_data.get('currentPathOfLegendSeasonResult', {}).get('trophies', 0)
    player2_bestPathOfLegendTrophies = player2_data.get('bestPathOfLegendSeasonResult', {}).get('trophies', 0)
    player2_clan = player2_data.get('clan', {}).get('name', 'No Clan')
    player2_evos, player2_num_of_evos = find_evos(player2_data)
    player2_wins = player2_data.get('wins', 0)
    player2_matches_played = player2_data.get('battleCount', 0)
    player2_win_rate = (player2_wins / player2_matches_played) * 100 if player2_matches_played > 0 else 0

    player2_current_rank_number = player2_data.get('currentPathOfLegendSeasonResult', {}).get('leagueNumber', 'N/A')
    player2_best_rank_number = player2_data.get('bestPathOfLegendSeasonResult', {}).get('leagueNumber', 'N/A')

    player2_current_rank_name = ranks.get(player2_current_rank_number, 'N/A')
    player2_highest_rank_name = ranks.get(player2_best_rank_number, 'N/A')

    player2_seasonal_arena = player2_data.get('progress', {}).get('seasonal-trophy-road-202510', {}).get('arena', {}).get('name', 'N/A')

    if player1_past_10k_trophies > 10000 and player2_past_10k_trophies > 10000:
        return f'Players🫅: {player1_name} | {player2_name}\n\nLevel 🌟: {player1_level} | {player2_level}\nTrophies 🏆: {player1_past_10k_trophies} | {player2_past_10k_trophies}\nBest Trophies 🥇: {player1_past_10k_best_trophies} | {player2_past_10k_best_trophies}\nCurrent Path Of Legends Trophies 🏅: {player1_currentPathOfLegendTrophies} | {player2_currentPathOfLegendTrophies}\nBest Path Of Legends Trophies ⚜️: {player1_bestPathOfLegendTrophies} | {player2_bestPathOfLegendTrophies}\nWin Rate 🟢: {math.ceil(player1_win_rate)}% | {math.ceil(player2_win_rate)}%\nClan 🏰: {player1_clan} | {player2_clan}\nSeasonal Arena 🏟️: {player1_seasonal_arena} | {player2_seasonal_arena}\nCurrent Rank 🔹: {player1_current_rank_name} | {player2_current_rank_name}\nHighest Rank 🔸: {player1_highest_rank_name} | {player2_highest_rank_name}'
    elif player1_past_10k_trophies > 10000 and player2_past_10k_trophies <= 10000:
        return f'Players🫅: {player1_name} | {player2_name}\n\nLevel 🌟: {player1_level} | {player2_level}\nTrophies 🏆: {player1_past_10k_trophies} | {player2_trophies}\nBest Trophies 🥇: {player1_past_10k_best_trophies} | {player2_best_trophies}\nCurrent Path Of Legends Trophies 🏅: {player1_currentPathOfLegendTrophies} | {player2_currentPathOfLegendTrophies}\nBest Path Of Legends Trophies ⚜️: {player1_bestPathOfLegendTrophies} | {player2_bestPathOfLegendTrophies}\nWin Rate 🟢: {math.ceil(player1_win_rate)}% | {math.ceil(player2_win_rate)}%\nClan 🏰: {player1_clan} | {player2_clan}\nArena ⚔️: {player1_arena} | {player2_arena}\nSeasonal Arena 🏟️: {player1_seasonal_arena} | {player2_seasonal_arena}\nCurrent Rank 🔹: {player1_current_rank_name} | {player2_current_rank_name}\nHighest Rank 🔸: {player1_highest_rank_name} | {player2_highest_rank_name}'
    elif player1_past_10k_trophies <= 10000 and player2_past_10k_trophies > 10000:
        return f'Players🫅: {player1_name} | {player2_name}\n\nLevel 🌟: {player1_level} | {player2_level}\nTrophies 🏆: {player1_trophies} | {player2_past_10k_trophies}\nBest Trophies 🥇: {player1_best_trophies} | {player2_past_10k_best_trophies}\nCurrent Path Of Legends Trophies 🏅: {player1_currentPathOfLegendTrophies} | {player2_currentPathOfLegendTrophies}\nBest Path Of Legends Trophies ⚜️: {player1_bestPathOfLegendTrophies} | {player2_bestPathOfLegendTrophies}\nWin Rate 🟢: {math.ceil(player1_win_rate)}% | {math.ceil(player2_win_rate)}%\nClan 🏰: {player1_clan} | {player2_clan}\nArena ⚔️: {player1_arena} | {player2_arena}\nSeasonal Arena 🏟️: {player1_seasonal_arena} | {player2_seasonal_arena}\nCurrent Rank 🔹: {player1_current_rank_name} | {player2_current_rank_name}\nHighest Rank 🔸: {player1_highest_rank_name} | {player2_highest_rank_name}'
    else:
        return f'Players 🫅: {player1_name} | {player2_name}\n\nLevel 🌟: {player1_level} | {player2_level}\nTrophies 🏆: {player1_trophies} | {player2_trophies}\nBest Trophies 🥇: {player1_best_trophies} | {player2_best_trophies}\nWin Rate 🟢: {math.ceil(player1_win_rate)}% | {math.ceil(player2_win_rate)}%\nArena ⚔️: {player1_arena} | {player2_arena}\nClan 🏰: {player1_clan} | {player2_clan}'

def jprint(data):
   text = json.dumps(data, sort_keys=True, indent=4)
   return text 
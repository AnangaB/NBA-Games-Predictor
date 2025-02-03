import time
import nba_api.stats.static.players as players
from nba_api.stats.endpoints import playercareerstats

import pandas as pd

all_players = pd.DataFrame(players.get_players())
all_players.to_csv(r"./../../Extracted Data/NBA Data/Players Stats/all_players.csv")

player_ids = all_players["id"].unique()
# Collect all player stats
all_player_stats_list = []
player_count = 0
total_player_length = len(player_ids)
for player_id in player_ids:
    player_data_received = False
    while player_data_received == False:
        try:
            # Fetch player career stats
            career = playercareerstats.PlayerCareerStats(player_id=player_id)
            stats = pd.DataFrame(career.get_data_frames()[0])
            if not stats.empty:
                all_player_stats_list.append(stats)
            player_data_received = True
        except Exception as e:
            print(f"Error fetching stats for player ID {player_id}: {e}. Now trying again...")
            time.sleep(5) 

    time.sleep(0.4) 
        
    player_count += 1
    print(f"Got data for {player_id}, and so done {player_count} out of {total_player_length}")


# Concatenate all collected DataFrames
all_player_stats = pd.concat(all_player_stats_list, ignore_index=True)

all_player_stats.to_csv(r"./../../Extracted Data/NBA Data/Players Stats/all_player_stats.csv")

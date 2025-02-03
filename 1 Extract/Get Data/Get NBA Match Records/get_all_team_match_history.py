from nba_api.stats.endpoints import teamgamelogs
import pandas as pd

seasons = [f"{v}-{str(v + 1)[-2:]}" for v in range(2000, 2024)]

season_df_list = []
print(seasons)
for season in seasons:
    season_data_received = False
    while not season_data_received:
        try:

            # Fetch data from the API
            team_game_logs = teamgamelogs.TeamGameLogs(season_nullable=season).get_data_frames()[0]
            
            season_df_list.append(team_game_logs)
            season_data_received = True
        
        except Exception as e:
            print(f"Error fetching team game logs: {e}")


pd.concat(season_df_list,ignore_index=True).to_csv(r"./../../Extracted Data/NBA Data/Team Stats/team_game_logs.csv")
    
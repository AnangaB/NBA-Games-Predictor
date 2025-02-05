from nba_api.stats.endpoints import BoxScoreAdvancedV3
import time
import pandas as pd

# Define file paths
output_file = r"./../../Extracted Data/NBA Data/Players Stats/all_players_stats_for_all_games.csv"
matches_file = r"./../../Extracted Data/NBA Data/Team Stats/team_game_logs.csv"


try:
    already_filled_data_set = pd.read_csv(output_file)
    filled_in_game_ids = already_filled_data_set["gameId"].unique()
except FileNotFoundError:
    already_filled_data_set = pd.DataFrame()
    filled_in_game_ids = []

matches_df = pd.read_csv(matches_file)
game_ids = ["00" + str(game_id) for game_id in matches_df["GAME_ID"].unique() if game_id not in filled_in_game_ids]

total_games = len(matches_df["GAME_ID"].unique())
num_games_extracted = len(filled_in_game_ids)

def update_output_file(all_players_stats_for_all_games_list, already_filled_data_set):
    """Writes combined data to the output file."""
    if all_players_stats_for_all_games_list:
        combined_data = pd.concat([already_filled_data_set] + all_players_stats_for_all_games_list, ignore_index=True)
        combined_data.to_csv(output_file, index=False)
        print(f"Data successfully written to {output_file}")

# Fetch and update data in batches
all_players_stats_for_all_games_list = []
batch_size = 50

for i, game_id in enumerate(game_ids, start=1):
    received_game_stats = False
    while not received_game_stats:
        try:
            print(f"Trying to fetch data for game {game_id}. This is {num_games_extracted} out of {total_games} so far.")
            
            # Fetch box score for the current game
            box_score = BoxScoreAdvancedV3(game_id=game_id)
            data = box_score.get_data_frames()[0]

            all_players_stats_for_all_games_list.append(data)

            received_game_stats = True
            num_games_extracted += 1

            # Write batch to file when batch_size is reached
            if i % batch_size == 0 or i == len(game_ids):
                update_output_file(all_players_stats_for_all_games_list, already_filled_data_set)
                already_filled_data_set = pd.concat([already_filled_data_set] + all_players_stats_for_all_games_list, ignore_index=True)
                all_players_stats_for_all_games_list.clear()

            time.sleep(.4)
        except Exception as e:
            print(f"Error fetching data: {e}. Retrying...")
            time.sleep(2)
import nba_api.stats.static.players as players
import pandas as pd

all_players = pd.DataFrame(players.get_players())
all_players.to_csv(r"./../../Extracted Data/NBA Data/Players Stats/all_players.csv")



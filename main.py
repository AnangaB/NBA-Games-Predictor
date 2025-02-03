from dotenv import load_dotenv
import os
from balldontlie import BalldontlieAPI

load_dotenv()

# Get the API key from environment variable
api_key = os.getenv("BDL_API_KEY")

api = BalldontlieAPI(api_key=api_key)
print(api.nba.teams.list())

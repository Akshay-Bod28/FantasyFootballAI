from fastapi import FastAPI, Body, Query
import joblib
import pandas as pd
from contextlib import asynccontextmanager

models = {}
datasets = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.models = {        #allows use outside of function
    'WR': joblib.load("app/saved_models/wr_model.pkl"),
    'RB': joblib.load("app/saved_models/rb_model.pkl"),
    'QB': joblib.load("app/saved_models/qb_model.pkl"),
    'TE': joblib.load("app/saved_models/te_model.pkl")
    }

    app.state.datasets = {
        "WR": pd.read_csv("app/data/wrStats.csv"),
        "RB": pd.read_csv("app/data/rb_stats.csv"),
        "QB": pd.read_csv("app/data/qb_stats.csv"),
        "TE": pd.read_csv("app/data/te_stats.csv")
    }
    yield  # App runs during this 

    #While app shuts down 
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",        # React development
    "http://3.145.60.140:4173"     # Your deployed frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # <- use this list
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
def predict_player(
    player_data: dict = Body(...),   #requires all
    position: str = Query(...),
    year: int = Query(...)
):
    position = position.upper()
    if position not in app.state.models:        #check that position is valid
        return {"error": f"Invalid position: {position}"}

    model = app.state.models[position]
    data = app.state.datasets[position]

    #filter player
    name = player_data.get("player_name", "Doesn't exist")   #gets player name from JSON
    player_info = data[data["player_name"].str.lower() == name.lower()]
    if player_info.empty:
        return {"error": f"Player {name} not found in {position} dataset"}

    #filter year
    if year not in player_info["season"].values:
        return {"error": f"Player {name} did not play in {year}"}
    player_info = player_info[player_info["season"] == year].copy()

    #feature columns per position
    feature_cols_per_position = {
        "WR": ["season","receiving_yards","yards_after_catch","rush_attempts","rush_touchdown","pass_touchdown","fumble","receptions","targets","receiving_touchdown","receptions_redzone","targets_redzone","receiving_touchdown_redzone","fantasy_points_ppr","offense_snaps","total_tds","touches","total_yards","games_missed","age","games_played_season"],
        "RB": ["season","receiving_yards","yards_after_catch","rush_attempts","rushing_yards","tackled_for_loss","rush_touchdown","pass_touchdown","fumble","receptions","targets","receiving_touchdown","receptions_redzone","targets_redzone","receiving_touchdown_redzone","rush_attempts_redzone","rush_touchdown_redzone","total_tds","touches","total_yards","age","games_played_season"],
        "QB": ["season","pass_attempts","complete_pass","passing_yards","rush_attempts","rushing_yards","rush_touchdown","pass_touchdown","safety","interception","fumble","fumble_lost","passing_air_yards","pass_attempts_redzone","complete_pass_redzone","pass_touchdown_redzone","rush_attempts_redzone","rush_touchdown_redzone","total_tds","touches","total_yards","games_missed","age","years_exp","games_played_season"],
        "TE": ["season","receiving_yards","yards_after_catch","rush_attempts","rushing_yards","rush_touchdown","fumble","fumble_lost","receptions","targets","receiving_air_yards","receiving_touchdown","receptions_redzone","targets_redzone","receiving_touchdown_redzone","offense_snaps","total_tds","total_yards","games_missed","age","games_played_season"]
    }

    feature_cols = feature_cols_per_position[position]

    #all CSV file columns
    feature_cols = [col for col in feature_cols if col in player_info.columns]
    if not feature_cols:
        return {"error": f"No valid feature columns found for {position} and player {name}"}

    #convert to all columns to numeric vals
    player_features = player_info[feature_cols].apply(pd.to_numeric, errors="coerce")

    #predict probability
    try:
        prob = float(model.predict_proba(player_features)[:, 1])
    except Exception as e:
        return {"error": f"Prediction failed: {str(e)}"}

    return {
        "player": name,
        "year": year,
        "position": position,
        "probability_top_10": prob
    }





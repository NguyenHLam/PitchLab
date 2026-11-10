"""
xG (Expected Goals) Model
=====================================================

OVERVIEW
-----------------------------------------------------
Expected goals (xG) is the probability that a given shot becomes a goal,
estimated from the circumstances of the shot, such as where it was taken,
with which body part, under pressure or not, etc. Summing xG over a player's
or team's shots shows how many goals they 'should' have scored, which can be
a better measure of chance quality than raw shot or goal counts.

This script builds an xG model as a binary classification problem:
    - Input: Features describing a single shot
    - Target: `is_goal` (0 = NO GOAL, 1 = GOAL)
    - Output: Calibrated probability between 0 and 1 for every shot

The goal is not just to separate goals from misses, but to produce well-
calibrated probabilities (shots given 0.20 xG should be scored roughly 20%
of the time).


DATA
-----------------------------------------------------
Source  :   StatsBomb Open Data, accessed through the `statesbombpy` package.
Scope   :   At startup the script lists every competition/season available in 
            the open data and asks user to pick one by number. Default if 2018
            FIFA World Cup (43/3).
Notes   :   Penalties are excluded due to being shot at a fixed distance
            with no defenders.


PITCH COORDINATES
-----------------------------------------------------
StatsBomb pitches are 120 x 80 units, and the attacking team always shoots
towards x = 120. The goal center is at (120, 40) and the posts are at
(120, 36) and (120, 44), meaning the goal mouth is 8 units wide.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsbombpy import sb

# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LogisticRegression
# from sklearn.ensemble import GradientBoostingClassifier
# from sklearn.metrics import roc_auc_score, brier_score_loss, log_loss
# from sklearn.calibration import calibration_curve
# from mplsoccer import Pitch

# Ignore statsbombpy credential warning
import warnings
warnings.filterwarnings("ignore", category=UserWarning) 

# -----------------------------------------------------
# (1) CONFIGURATION
# -----------------------------------------------------
COMPETITION_ID = 43
SEASON_ID = 3
RANDOM_STATE = 42

GOAL_X = 120.0
GOAL_Y = 40.0
POST_LEFT_Y = 36.0
POST_RIGHT_Y = 44.0

def choose_competiton() -> tuple[int, int]:
    """
    List every competition/season in the StatsBomb open data and let the user pick
    one by number. Returns (competition_id, season_id). Pressing ENTER or running
    without a terminal uses default (43, 3): FIFA World Cup 2018.
    """
    comps = sb.competitions()[
        ["competition_id", "season_id", "competition_name", "season_name"]
    ]
    
    comps = comps.sort_values(
        ["competition_name", "season_name"], ascending=[True, False]
    ).reset_index(drop=True)

    print("\nAvailable competitions (StatsBomb open data):\n")
    print(comps[["competition_name", "season_name"]].to_string())

    is_default = (comps["competition_id"] == COMPETITION_ID) & (comps["season_id"] == SEASON_ID)
    default_row = int(comps.index[is_default][0]) if is_default.any() else None

    while (True):
        prompt = "\nEnter the row number to use"
        if (default_row is not None):
            row = default_row
        try:
            choice = input(prompt + ": ").strip()
        except EOFError:
            choice = ""
        
        if (choice == "" and default_row is not None):
            row = default_row
        elif (choice.isdigit() and int(choice) in comps.index):
            row = int(choice)
        else:
            print(f"Invalid choice. Enter a number between 0 and {len(comps) - 1}.")
            continue
        
        picked = comps.loc[row]
        print(f"Using: {picked['competition_name']} {picked['season_name']}")
        return (int(picked["competition_id"]), int(picked["season_id"]))


# -----------------------------------------------------
# (2) LOAD MATCHES AND SHOT EVENTS
# -----------------------------------------------------
def load_shots(competition_id: int, season_id: int) -> pd.DataFrame:
    """
    Download all events for a competition/season and return only shots.
    """
    matches = sb.matches(competition_id=competition_id, season_id=season_id)
    print(f"Found {len(matches)} matches. Please wait for events to download...")

    shot_frames = []
    for match_id in matches["match_id"]:
        events = sb.events(match_id=match_id)
        shots = events[events["type"] == "Shot"].copy()
        shots["match_id"] = match_id
        shot_frames.append(shots)
    
    return pd.concat(shot_frames, ignore_index=True)


# -----------------------------------------------------
# (3) CLEAN SHOTS
# -----------------------------------------------------
def clean_shots(shots: pd.DataFrame) -> pd.DataFrame:
    """
    Keep the columns we need, split the location into (x,y), create the binary
    target `is_goal`, and drop penalty shots, which have different xG from open
    play and are often modelled separately.
    """
    df = shots.copy()

    df = df[df["shot_type"] != "Penalty"]
    
    df["x"] = df["location"].apply(lambda loc: loc[0])
    df["y"] = df["location"].apply(lambda loc: loc[1])

    df["is_goal"] = (df["shot_outcome"] == "Goal").astype(int)

    keep = [
        "match_id", "player", "team", "x", "y", "is_goal",
        "shot_body_part", "shot_technique", "shot_type", "under_pressure",
        "shot_statsbomb_xg" # StatBomb's own xG, useful as a benchmark
    ]
    df = df[keep].reset_index(drop=True)

    # under_pressure is NaN when False
    df["under_pressure"] = df["under_pressure"].fillna(False).astype(int)

    return df


# -----------------------------------------------------
# MAIN PIPELINE
# -----------------------------------------------------
def main() -> None:
    competition_id, season_id = choose_competiton()
    raw_shots = load_shots(competition_id, season_id)
    shots = clean_shots(raw_shots)
    print(f"{len(shots)} open-play shots, goal rate = {shots['is_goal'].mean():.3f}")


if __name__ == "__main__":
    main()
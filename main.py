import subprocess
import sys

# Function to install a package using pip
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# List of required packages
packages = [
    "statsbombpy"
]

# Install all required packages
for package in packages:
    install(package)






import streamlit as st
from statsbombpy import sb
import pandas as pd
from mplsoccer import Pitch
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import freeze_support

def fetch_data():
    # Accessing data from Statsbomb
    events_df = sb.competition_events(
        country="Germany",
        division="1. Bundesliga",
        season="2023/2024",
        gender="male"
    )

    frames_df = sb.competition_frames(
        country="Germany",
        division="1. Bundesliga",
        season="2023/2024",
        gender="male"
    )

    frames_df.rename(columns={'event_uuid': 'id'}, inplace=True)
    merged_df = pd.merge(frames_df, events_df, how="left", on=["match_id", "id"])

    return merged_df

def main():
    # Fetch data
    merged_df = fetch_data()

    # Filter data for Bayer Leverkusen
    BayerL = merged_df[merged_df['team'] == 'Bayer Leverkusen']

    # Function to convert lists to tuples, leave other types unchanged
    def convert_to_tuple(x):
        if isinstance(x, list):
            return tuple(x)
        return x

    BayerL['pass_end_location'] = BayerL['pass_end_location'].apply(convert_to_tuple)
    BayerL['location_y'] = BayerL['location_y'].apply(convert_to_tuple)

    # Filter passes
    BayerL_Pass = BayerL[BayerL['type'] == 'Pass']

    # Select relevant columns and drop duplicates
    BayerL_Pass = BayerL_Pass[['match_id', 'minute', 'location_y', 
                               'pass_end_location', 'period', 'player', 
                               'pass_recipient', 'pass_type', 'pass_length',
                               'second', 'timestamp']].drop_duplicates()

    # Extract x, y, endx, endy coordinates
    BayerL_Pass['x'] = BayerL_Pass['location_y'].apply(lambda loc: loc[0])
    BayerL_Pass['endx'] = BayerL_Pass['pass_end_location'].apply(lambda loc: loc[0])
    BayerL_Pass['y'] = BayerL_Pass['location_y'].apply(lambda loc: loc[1])
    BayerL_Pass['endy'] = BayerL_Pass['pass_end_location'].apply(lambda loc: loc[1])

    # Streamlit app
    st.title("Bayer Leverkusen's Pass Analysis")

    # Dropdown for player, match_id, time_from, and time_to
    player = st.selectbox('Select the player', ['', *BayerL_Pass['player'].unique()])
    match_id = st.selectbox('Select the match ID', BayerL_Pass['match_id'].unique())
    time_from = st.slider('Select the start minute', 0, BayerL_Pass['minute'].max() + 1, 0)
    time_to = st.slider('Select the end minute', 0, BayerL_Pass['minute'].max() + 1, BayerL_Pass['minute'].max() + 1)

    # Set up the pitch
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
    fig, ax = pitch.draw(figsize=(16, 11), constrained_layout=True, tight_layout=False)
    fig.set_facecolor('#22312b')

    if player == '':
        st.subheader(f"Bayer Leverkusen's Passes in match-{match_id}")
        # Filter the DataFrame based on the user input
        df = BayerL_Pass[(BayerL_Pass['match_id'] == match_id) & 
                         (BayerL_Pass['minute'] >= time_from) & 
                         (BayerL_Pass['minute'] <= time_to)]
    else:
        st.subheader(f"Bayer Leverkusen's {player} Passes in match-{match_id}")
        # Filter the DataFrame based on the user input
        df = BayerL_Pass[(BayerL_Pass['player'] == player) &
                         (BayerL_Pass['match_id'] == match_id) & 
                         (BayerL_Pass['minute'] >= time_from) & 
                         (BayerL_Pass['minute'] <= time_to)]

    for i in range(len(df)):
        ax.plot((df.iloc[i]['x'], df.iloc[i]['endx']), (df.iloc[i]['y'], df.iloc[i]['endy']), color="green")
        ax.scatter(df.iloc[i]['x'], df.iloc[i]['y'], color='green')
        ax.text(df.iloc[i]['x'], df.iloc[i]['y'], f'Pass-{i+1}', color='white', fontsize=10)

    st.pyplot(fig)

if __name__ == '__main__':
    freeze_support()  # Ensures proper initialization on Windows
    main()

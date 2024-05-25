import subprocess
import sys

# Function to install a package using pip
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", package])

# List of required packages
packages = [
    "streamlit",
    "pandas",
    "mplsoccer",
    "numpy",
    "matplotlib"
]
import streamlit as st
import pandas as pd
from mplsoccer import Pitch
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import freeze_support


def main():
    BayerL_Pass=pd.read_csv(r"C:\Users\preci\BayerL_Pass.csv")



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

import subprocess
import sys

# Function to install a package using pip
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# List of required packages
packages = [
    "streamlit",
    "pandas",
    "mplsoccer",
    "numpy",
    "matplotlib",
    "plotly"
]

# Install all required packages
for package in packages:
    try:
        install(package)
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package}: {e}")

# Now the rest of your script can assume that these packages are installed
import streamlit as st
# from statsbombpy import sb
import pandas as pd
from mplsoccer import Pitch
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import freeze_support
import plotly.express as px

def main():
    BayerL_Pass=pd.read_csv(r"BayerL_Pass.csv")



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
    

    # Plot interactive bar graph for number of passes by each player
    pass_counts = df['player'].value_counts().reset_index()
    pass_counts.columns = ['Player', 'Number of Passes']

    fig = px.bar(pass_counts, x='Player', y='Number of Passes', title='Number of Passes by Each Player')
    st.plotly_chart(fig)

if __name__ == '__main__':
    freeze_support()  # Ensures proper initialization on Windows
    main()

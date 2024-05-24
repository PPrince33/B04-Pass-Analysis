# Bayer Leverkusen Passes Visualization
This repository contains a Python script to visualize the passes made by Bayer Leverkusen players in a specific match, within a given time frame. The visualization uses the mplsoccer library and leverages data from the StatsBomb API.

### Features
* Visualizes passes on a football pitch.
* Filters passes by player name, match ID, and minute range.
* Displays pass trajectories and starting points.
* Uses Streamlit for an interactive web interface.
* Option to select inputs using Questionary and Tkinter.

### Requirements
* Python 3.7+
* matplotlib
* mplsoccer
* pandas
* streamlit
* statsbombpy
* questionary
* tkinter

### License
This project is licensed under the MIT License. See the LICENSE file for details.

### Acknowledgements
This script uses the 'mplsoccer' library for creating the pitch visualization.
Data is sourced from the StatsBomb API.


### Data Retrieval

Ensure you have access to the StatsBomb API. Use the following code to retrieve event and frame data for the Bundesliga 2023/2024 season:

```python
from statsbombpy import sb

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
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- This script uses the `mplsoccer` library for creating the pitch visualization.
- Data is sourced from the StatsBomb API.

---

Feel free to customize the README further based on your specific needs and preferences.

import streamlit as st
import requests
import pandas as pd
import json

st.set_page_config(page_title='Dynasty Football MVP', layout='wide')
st.sidebar.title('Dynasty Toolkit')
section = st.sidebar.radio('Navigate to:', [
    'Team Roster', 'Lineup Optimizer', 'Trade Finder', 'Draft Pick Tracker']
)

st.title('Dynasty Football Management')
LEAGUE_ID = '1181770802822885376'
USERNAME = 'burkex12'

def fetch_json(url):
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return res.json()
    except:
        return None
    return None

# Load league data once
rosters = fetch_json(f'https://api.sleeper.app/v1/league/{LEAGUE_ID}/rosters')
users = fetch_json(f'https://api.sleeper.app/v1/league/{LEAGUE_ID}/users')
player_map = fetch_json('https://api.sleeper.app/v1/players/nfl')

user_id, my_players, taxi_ids = None, [], []
if users:
    for u in users:
        display = (u.get('display_name') or '').lower()
        uname = (u.get('metadata', {}).get('username') or '').lower()
        if display == USERNAME.lower() or uname == USERNAME.lower():
            user_id = u.get('user_id')
            break
if rosters and user_id:
    for r in rosters:
        if r.get('owner_id') == user_id:
            my_players = r.get('players', [])
            taxi_ids = r.get('taxi', [])
            break

def get_player_data(pid):
    p = player_map.get(pid, {})
    return {
        'Name': p.get('full_name', pid),
        'Position': p.get('position', ''),
        'Team': p.get('team', ''),
        'Age': p.get('age', ''),
        'Taxi': 'Yes' if pid in taxi_ids else ''
    }

if section == 'Team Roster':
    st.subheader('Your Dynasty Roster (Taxi noted)')
    if my_players and player_map:
        data = [get_player_data(pid) for pid in my_players]
        st.dataframe(pd.DataFrame(data))
    else:
        st.warning('Roster not available.')

elif section == 'Lineup Optimizer':
    st.subheader('Optimized Lineup — Format: 1QB, 2RB, 3WR, 1TE, 2FLEX, 1SUPERFLEX')
    if my_players and player_map:
        df = pd.DataFrame([get_player_data(pid) for pid in my_players])
        positions = {
            'QB': df[df['Position'] == 'QB'],
            'RB': df[df['Position'] == 'RB'],
            'WR': df[df['Position'] == 'WR'],
            'TE': df[df['Position'] == 'TE'],
        }
        lineup = pd.concat([
            positions['QB'].head(1),
            positions['RB'].head(2),
            positions['WR'].head(3),
            positions['TE'].head(1),
            df[~df['Position'].isin(['QB'])].head(2),
            df.head(1)  # Superflex any
        ])
        st.dataframe(lineup.reset_index(drop=True))
    else:
        st.warning('Lineup could not be generated.')

elif section == 'Trade Finder':
    st.subheader('Rebuild Strategy Trade Finder')
    if my_players and player_map:
        df = pd.DataFrame([get_player_data(pid) for pid in my_players])
        aging = df[df['Age'].apply(lambda x: isinstance(x, int) and x >= 28)]
        suggestions = pd.DataFrame([
            {'Trade Away': row['Name'], 'Suggested Return': 'Pick or Young Player'}
            for _, row in aging.iterrows()
        ])
        st.dataframe(suggestions.reset_index(drop=True))
    else:
        st.warning('Trade suggestions unavailable — missing roster data.')

elif section == 'Draft Pick Tracker':
    st.subheader('Draft Pick Ownership')
    st.table(pd.DataFrame([
        {'Team': 'You', '2025 1st': 'Own', '2025 2nd': 'Own', '2025 3rd': 'Traded'},
        {'Team': 'Team B', '2025 1st': 'Traded', '2025 2nd': 'Own', '2025 3rd': 'Own'},
        {'Team': 'Team C', '2025 1st': 'Own', '2025 2nd': 'Own', '2025 3rd': 'Own'}
    ]))

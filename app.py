import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title='Dynasty Football MVP', layout='wide')
st.sidebar.title('Dynasty Toolkit')
section = st.sidebar.radio('Navigate to:', [
    'Team Roster', 'Lineup Optimizer', 'Trade Finder', 'Draft Pick Tracker']
)

st.title('Dynasty Football Management Dashboard')
LEAGUE_ID = '1181770802822885376'
USERNAME = 'burkex12'

def fetch_json(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

rosters = fetch_json(f'https://api.sleeper.app/v1/league/{LEAGUE_ID}/rosters')
users = fetch_json(f'https://api.sleeper.app/v1/league/{LEAGUE_ID}/users')
player_map = fetch_json('https://api.sleeper.app/v1/players/nfl')

user_id, my_players, taxi_ids = None, [], []
if users:
    for u in users:
        if (u.get('display_name') or '').lower() == USERNAME or (u.get('metadata', {}).get('username') or '').lower() == USERNAME:
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

df = pd.DataFrame([get_player_data(pid) for pid in my_players]) if my_players else pd.DataFrame()

if section == 'Team Roster':
    st.subheader('Team Roster with Taxi Squad')
    if not df.empty:
        st.dataframe(df)
    else:
        st.warning('No roster data available.')

elif section == 'Lineup Optimizer':
    st.subheader('Lineup Optimizer')
    if not df.empty:
        pos = lambda p: df[df['Position'] == p]
        superflex_pool = df.copy()
        lineup = pd.concat([
            pos('QB').head(1),
            pos('RB').head(2),
            pos('WR').head(3),
            pos('TE').head(1),
            df[df['Position'].isin(['RB','WR','TE'])].iloc[4:6],
            superflex_pool.iloc[0:1]
        ])
        st.dataframe(lineup.reset_index(drop=True))
    else:
        st.warning('No players available for optimization.')

elif section == 'Trade Finder':
    st.subheader('Rebuild Strategy Trade Finder')
    user_input = st.text_input('Enter players or picks to trade (comma separated):')
    if user_input:
        tradeables = [x.strip() for x in user_input.split(',') if x.strip()]
        results = pd.DataFrame([
            {'You Give': name, 'You Get': 'Young player or future pick'}
            for name in tradeables
        ])
        st.dataframe(results)
    else:
        if not df.empty:
            aging = df[df['Age'].apply(lambda x: isinstance(x, int) and x >= 28)]
            rebuild_suggestions = pd.DataFrame([
                {'Trade Away': row['Name'], 'Suggested Return': 'Pick or young player'}
                for _, row in aging.iterrows()
            ])
            st.dataframe(rebuild_suggestions.reset_index(drop=True))
        else:
            st.info('No input provided and no roster loaded.')

elif section == 'Draft Pick Tracker':
    st.subheader('Draft Pick Ownership (2025 Mock)')
    picks = [
        {'Team': 'You', '2025 1st': 'Own', '2025 2nd': 'Own', '2025 3rd': 'Traded'},
        {'Team': 'Team B', '2025 1st': 'Traded', '2025 2nd': 'Own', '2025 3rd': 'Own'},
        {'Team': 'Team C', '2025 1st': 'Own', '2025 2nd': 'Own', '2025 3rd': 'Own'}
    ]
    st.dataframe(pd.DataFrame(picks))

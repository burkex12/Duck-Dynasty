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

if section == 'Team Roster':
    st.subheader('Your Dynasty Roster (Taxi noted)')
    rosters = fetch_json(f'https://api.sleeper.app/v1/league/{LEAGUE_ID}/rosters')
    users = fetch_json(f'https://api.sleeper.app/v1/league/{LEAGUE_ID}/users')
    player_map = fetch_json('https://api.sleeper.app/v1/players/nfl')

    user_id = None
    if users:
        for u in users:
            name = (u.get('display_name') or '').lower()
            uname = (u.get('metadata', {}).get('username') or '').lower()
            if name == USERNAME.lower() or uname == USERNAME.lower():
                user_id = u.get('user_id')
                break

    if rosters and user_id and player_map:
        player_ids, taxi_ids = [], []
        for r in rosters:
            if r.get('owner_id') == user_id:
                player_ids = r.get('players', [])
                taxi_ids = r.get('taxi', [])
                break
        data = []
        for pid in player_ids:
            p = player_map.get(pid, {})
            data.append({
                'Name': p.get('full_name', pid),
                'Position': p.get('position', ''),
                'Team': p.get('team', ''),
                'Age': p.get('age', ''),
                'Taxi': 'Yes' if pid in taxi_ids else ''
            })
        st.dataframe(pd.DataFrame(data))
    else:
        st.warning('Could not load roster or user.')

elif section == 'Lineup Optimizer':
    st.subheader('Lineup Optimizer — Format: 1QB, 2RB, 3WR, 1TE, 2FLEX, 1SUPERFLEX')
    demo_lineup = [
        {'Name': 'Patrick Mahomes', 'Pos': 'QB'},
        {'Name': 'Breece Hall', 'Pos': 'RB'},
        {'Name': 'Jahmyr Gibbs', 'Pos': 'RB'},
        {'Name': 'Garrett Wilson', 'Pos': 'WR'},
        {'Name': 'Chris Olave', 'Pos': 'WR'},
        {'Name': 'Drake London', 'Pos': 'WR'},
        {'Name': 'Kyle Pitts', 'Pos': 'TE'},
        {'Name': 'Puka Nacua', 'Pos': 'FLEX'},
        {'Name': 'Jayden Reed', 'Pos': 'FLEX'},
        {'Name': 'Tua Tagovailoa', 'Pos': 'SUPERFLEX'}
    ]
    st.table(pd.DataFrame(demo_lineup))

elif section == 'Trade Finder':
    st.subheader('Trade Finder — Rebuild Strategy')
    st.write('Trade aging/prime players for youth and future picks.')
    trades = [
        {'Give': 'Derrick Henry', 'Get': 'Tyjae Spears + 2025 2nd'},
        {'Give': 'Davante Adams', 'Get': 'Quentin Johnston + 2025 1st'},
        {'Give': 'Alvin Kamara', 'Get': 'Tank Bigsby + 2025 2nd'},
        {'Give': 'Keenan Allen', 'Get': 'Rashee Rice + 2025 1st'}
    ]
    st.table(pd.DataFrame(trades))

elif section == 'Draft Pick Tracker':
    st.subheader('Draft Pick Ownership')
    picks = [
        {'Team': 'You', '2025 1st': 'Own', '2025 2nd': 'Own', '2025 3rd': 'Traded'},
        {'Team': 'Team B', '2025 1st': 'Traded', '2025 2nd': 'Own', '2025 3rd': 'Own'},
        {'Team': 'Team C', '2025 1st': 'Own', '2025 2nd': 'Own', '2025 3rd': 'Own'}
    ]
    st.table(pd.DataFrame(picks))

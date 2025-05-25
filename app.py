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
    st.subheader('Your Dynasty Roster')
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
        player_ids = []
        for r in rosters:
            if r.get('owner_id') == user_id:
                player_ids = r.get('players', [])
                break
        data = []
        for pid in player_ids:
            p = player_map.get(pid, {})
            data.append({
                'Name': p.get('full_name', pid),
                'Position': p.get('position', ''),
                'Team': p.get('team', ''),
                'Age': p.get('age', '')
            })
        st.dataframe(pd.DataFrame(data))
    else:
        st.warning('Could not load roster or user.')

elif section == 'Lineup Optimizer':
    st.subheader('Lineup Optimizer')
    st.write('Based on a 1QB, 2RB, 2WR, 1TE, 2FLEX format.')
    demo_lineup = [
        {'Name': 'Patrick Mahomes', 'Pos': 'QB'},
        {'Name': 'Christian McCaffrey', 'Pos': 'RB'},
        {'Name': 'Saquon Barkley', 'Pos': 'RB'},
        {'Name': 'Justin Jefferson', 'Pos': 'WR'},
        {'Name': 'CeeDee Lamb', 'Pos': 'WR'},
        {'Name': 'Mark Andrews', 'Pos': 'TE'},
        {'Name': 'Amon-Ra St. Brown', 'Pos': 'FLEX'},
        {'Name': 'Bijan Robinson', 'Pos': 'FLEX'},
    ]
    st.table(pd.DataFrame(demo_lineup))

elif section == 'Trade Finder':
    st.subheader('Trade Suggestions')
    st.write('Demo: Depth trade recommendation example')
    st.info('You have 5 WRs and only 2 RBs. Consider trading a WR for RB depth.')
    st.markdown('**Suggested Trade**: Courtland Sutton for James Conner')

elif section == 'Draft Pick Tracker':
    st.subheader('Draft Pick Ownership')
    st.write('Demo data for 2025 picks')
    picks = [
        {'Team': 'You', 'Round 1': 'Own', 'Round 2': 'Own', 'Round 3': 'Traded'},
        {'Team': 'Team B', 'Round 1': 'Traded', 'Round 2': 'Own', 'Round 3': 'Own'},
        {'Team': 'Team C', 'Round 1': 'Own', 'Round 2': 'Traded', 'Round 3': 'Own'},
    ]
    st.table(pd.DataFrame(picks))

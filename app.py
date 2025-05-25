import streamlit as st
import requests
import json

st.set_page_config(page_title='Dynasty Football Tool', layout='wide', initial_sidebar_state='expanded')
st.markdown('<style>body { font-family: "Segoe UI", sans-serif; } .block-container { padding-top: 2rem; }</style>', unsafe_allow_html=True)
st.sidebar.title('Dynasty Football Dashboard')
section = st.sidebar.radio('Navigate to:', [
    'Team Roster', 'Lineup Optimizer', 'Trade Finder', 'Draft Pick Tracker']
)

st.title('Dynasty Football Management')
st.caption('Powered by Sleeper API | Built for League ID: 1181770802822885376')

LEAGUE_ID = '1181770802822885376'
USERNAME = 'burkex12'

def fetch_json(url):
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return res.json()
        return None
    except:
        return None

if section == 'Team Roster':
    st.subheader('Your Dynasty Team')
    rosters = fetch_json(f'https://api.sleeper.app/v1/league/{LEAGUE_ID}/rosters')
    users = fetch_json(f'https://api.sleeper.app/v1/league/{LEAGUE_ID}/users')
    player_map = fetch_json('https://api.sleeper.app/v1/players/nfl')

    user_id = None
    if users:
        for u in users:
            display = (u.get('display_name') or '').lower()
            meta = (u.get('metadata', {}).get('username') or '').lower()
            if display == USERNAME.lower() or meta == USERNAME.lower():
                user_id = u.get('user_id')
                break

    player_ids = []
    if rosters and user_id:
        for r in rosters:
            if r.get('owner_id') == user_id:
                player_ids = r.get('players', [])
                break
        if player_ids and player_map:
            names = [
                f"{player_map.get(pid, {}).get('full_name', pid)} — {player_map.get(pid, {}).get('position', '')}"
                for pid in player_ids
            ]
            st.success('Your current roster:')
            st.write(names)
        else:
            st.warning('No player data found.')
    else:
        st.warning('Unable to load user or roster info.')

elif section == 'Lineup Optimizer':
    st.subheader('Lineup Optimizer')
    st.info('Coming soon: Your optimal weekly starters based on projections.')

elif section == 'Trade Finder':
    st.subheader('Trade Finder')
    st.info('Coming soon: Explore fair trades based on team needs.')

elif section == 'Draft Pick Tracker':
    st.subheader('Draft Pick Tracker')
    st.info('Coming soon: Full draft pick ownership and tracking.')

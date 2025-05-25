import streamlit as st
import requests
import json

st.set_page_config(page_title='Dynasty Football Tool')
st.sidebar.title('Dynasty Toolkit')
debug_mode = st.sidebar.checkbox('Debug Mode')
section = st.sidebar.radio('Navigate to:', [
    'My Team', 'Lineup Optimizer', 'Trade Finder', 'Draft Pick Tracker']
)

st.title('Dynasty Football Management MVP')

league_id = '1181770802822885376'
username = 'burkex12'

def fetch_json(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f'Failed to fetch from {url} — Status {response.status_code}')
            return None
    except Exception as e:
        st.error(f'Exception fetching {url}: {e}')
        return None

if section == 'My Team':
    st.header('My Team')
    st.write('Loading your real roster from Sleeper...')
    rosters = fetch_json(f'https://api.sleeper.app/v1/league/{league_id}/rosters')
    users = fetch_json(f'https://api.sleeper.app/v1/league/{league_id}/users')
    player_map = fetch_json('https://api.sleeper.app/v1/players/nfl')

    if debug_mode:
        st.subheader('Debug Output')
        st.code(json.dumps({'users': users, 'rosters': rosters}, indent=2))

    user_id = None
    if users:
        for u in users:
            display = (u.get('display_name') or '').lower()
            meta_name = (u.get('metadata', {}).get('username') or '').lower()
            if display == username.lower() or meta_name == username.lower():
                user_id = u.get('user_id')
                break
    else:
        st.error('User list was empty or unavailable.')

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
            st.success('Your team:')
            st.write(names)
        elif not player_ids:
            st.warning('No players found for your roster.')
    elif not user_id:
        st.error('Your user ID could not be determined from the league.')

elif section == 'Lineup Optimizer':
    st.header('Lineup Optimizer')
    st.write('Coming soon: Optimal lineup projection.')

elif section == 'Trade Finder':
    st.header('Trade Finder')
    st.write('Coming soon: Trade suggestions based on value tiers.')

elif section == 'Draft Pick Tracker':
    st.header('Draft Pick Tracker')
    st.write('Coming soon: Track league pick ownership.')

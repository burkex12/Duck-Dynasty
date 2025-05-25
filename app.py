import streamlit as st
import requests

st.set_page_config(page_title='Dynasty Football Tool')

st.sidebar.title('Dynasty Toolkit')
section = st.sidebar.radio('Navigate to:', [
    'My Team', 'Lineup Optimizer', 'Trade Finder', 'Draft Pick Tracker']
)

st.title('Dynasty Football Management MVP')

# Hardcoded user setup
league_id = '918911833332760576'
players_data = {}

if section == 'My Team':
    st.header('My Team')
    st.write('Loading your real roster from Sleeper...')
    try:
        rosters = requests.get(f'https://api.sleeper.app/v1/league/{league_id}/rosters').json()
        users = requests.get(f'https://api.sleeper.app/v1/league/{league_id}/users').json()
        user_id = None
        for u in users:
            if u.get('display_name', '').lower() == 'burkex12':
                user_id = u['user_id']
                break
        player_ids = []
        for r in rosters:
            if r['owner_id'] == user_id:
                player_ids = r.get('players', [])
                break
        if player_ids:
            player_map = requests.get('https://api.sleeper.app/v1/players/nfl').json()
            names = [f"{player_map.get(pid, {}).get('full_name', pid)} — {player_map.get(pid, {}).get('position', '')}" for pid in player_ids]
            st.success('Your team:')
            st.write(names)
        else:
            st.warning('No players found for this user in league.')
    except Exception as e:
        st.error(f'Error loading team: {e}')

elif section == 'Lineup Optimizer':
    st.header('Lineup Optimizer')
    st.write('Coming soon: Optimized lineup from your active roster.')

elif section == 'Trade Finder':
    st.header('Trade Finder')
    st.write('Coming soon: Suggest trades based on depth and value.')

elif section == 'Draft Pick Tracker':
    st.header('Draft Pick Tracker')
    st.write('Coming soon: View future pick ownership.')

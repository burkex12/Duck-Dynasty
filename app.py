import streamlit as st
import requests

st.set_page_config(page_title='Dynasty Football Tool')

st.sidebar.title('Dynasty Toolkit')
section = st.sidebar.radio('Navigate to:', [
    'Dashboard', 'Sleeper Sync', 'My Team', 'Lineup Optimizer', 'Trade Finder', 'Draft Pick Tracker']
)

st.title('Dynasty Football Management MVP')

# Global placeholder for user and league data
if 'league_id' not in st.session_state:
    st.session_state['league_id'] = None
if 'roster' not in st.session_state:
    st.session_state['roster'] = []

if section == 'Sleeper Sync':
    st.header('Sleeper Integration')
    username = st.text_input('Enter Sleeper Username:')
    if st.button('Sync League') and username:
        user_req = requests.get(f'https://api.sleeper.app/v1/user/{username}')
        if user_req.status_code == 200:
            user_id = user_req.json().get('user_id')
            leagues_req = requests.get(
                f'https://api.sleeper.app/v1/user/{user_id}/leagues/nfl/2024')
            if leagues_req.status_code == 200:
                leagues = leagues_req.json()
                if leagues:
                    st.session_state['league_id'] = leagues[0]['league_id']
                    st.success(f'League synced: {leagues[0]["name"]}')
                else:
                    st.warning('No leagues found for this user.')
            else:
                st.error('Failed to fetch leagues.')
        else:
            st.error('Invalid Sleeper username.')

elif section == 'My Team':
    st.header('My Team')
    league_id = st.session_state.get('league_id')
    if league_id:
        rosters_req = requests.get(f'https://api.sleeper.app/v1/league/{league_id}/rosters')
        if rosters_req.status_code == 200:
            rosters = rosters_req.json()
            user_id = requests.get(f'https://api.sleeper.app/v1/league/{league_id}').json()['user_id']
            for r in rosters:
                if r['owner_id'] == user_id:
                    st.session_state['roster'] = r['players']
                    break
        if st.session_state['roster']:
            st.success('Your players:')
            st.write(st.session_state['roster'])
        else:
            st.warning('Could not find your team in this league.')
    else:
        st.warning('Please sync your Sleeper account first.')

elif section == 'Dashboard':
    st.header('League Dashboard')
    st.write('Overview of your league.')

elif section == 'Lineup Optimizer':
    st.header('Lineup Optimizer')
    st.write('Coming soon: Best starting lineup based on projections.')

elif section == 'Trade Finder':
    st.header('Trade Finder')
    st.write('Coming soon: Suggest trades based on team needs and values.')

elif section == 'Draft Pick Tracker':
    st.header('Draft Pick Tracker')
    st.write('Coming soon: Pick ownership across all league teams.')

import streamlit as st
import requests

st.set_page_config(page_title='Dynasty Football Tool')

st.sidebar.title('Dynasty Toolkit')
section = st.sidebar.radio('Navigate to:', [
    'Dashboard', 'Sleeper Sync', 'My Team', 'Lineup Optimizer', 'Trade Finder', 'Draft Pick Tracker']
)

st.title('Dynasty Football Management MVP')

# Initialize session state
for key in ['user_id', 'league_id', 'roster']:
    if key not in st.session_state:
        st.session_state[key] = None if key != 'roster' else []

if section == 'Sleeper Sync':
    st.header('Sleeper Integration')
    username = st.text_input('Enter Sleeper Username:')
    if st.button('Sync League') and username:
        user_req = requests.get(f'https://api.sleeper.app/v1/user/{username}')
        if user_req.status_code == 200:
            user_id = user_req.json().get('user_id')
            st.session_state['user_id'] = user_id
            leagues_req = requests.get(f'https://api.sleeper.app/v1/user/{user_id}/leagues/nfl/2024')
            if leagues_req.status_code == 200:
                leagues = leagues_req.json()
                if leagues:
                    league_id = leagues[0]['league_id']
                    st.session_state['league_id'] = league_id
                    st.success(f'Successfully synced: {leagues[0]["name"]}')
                else:
                    st.warning('No leagues found.')
            else:
                st.error('Could not retrieve leagues.')
        else:
            st.error('Invalid Sleeper username.')

elif section == 'My Team':
    st.header('My Team')
    league_id = st.session_state.get('league_id')
    user_id = st.session_state.get('user_id')
    if league_id and user_id:
        rosters_req = requests.get(f'https://api.sleeper.app/v1/league/{league_id}/rosters')
        if rosters_req.status_code == 200:
            rosters = rosters_req.json()
            for r in rosters:
                if r['owner_id'] == user_id:
                    st.session_state['roster'] = r.get('players', [])
                    break
        if st.session_state['roster']:
            st.success('Your team roster:')
            st.write(st.session_state['roster'])
        else:
            st.warning('Could not match user to a team in this league.')
    else:
        st.warning('Sync your Sleeper account first.')

elif section == 'Dashboard':
    st.header('League Dashboard')
    st.write('Overview of your league.')

elif section == 'Lineup Optimizer':
    st.header('Lineup Optimizer')
    st.write('Coming soon: Optimal lineup projection.')

elif section == 'Trade Finder':
    st.header('Trade Finder')
    st.write('Coming soon: Trade suggestions based on value tiers.')

elif section == 'Draft Pick Tracker':
    st.header('Draft Pick Tracker')
    st.write('Coming soon: Track league pick ownership.')

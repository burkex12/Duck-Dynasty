import streamlit as st

st.set_page_config(page_title='Dynasty Football Tool')

st.sidebar.title('Navigation')
selection = st.sidebar.radio('Go to', [
    'Dashboard', 'Sleeper Login & Sync', 'Lineup Optimizer', 'Trade Finder', 'Draft Pick Tracker'])

st.title('Dynasty Football Management MVP')

if selection == 'Dashboard':
    st.header('League Dashboard')
    st.write('Overview of your synced Sleeper league, roster stats, and team summaries.')

elif selection == 'Sleeper Login & Sync':
    st.header('Sleeper Integration')
    username = st.text_input('Enter your Sleeper username:')
    if st.button('Sync League'):
        st.success(f'Simulated sync with Sleeper account: {username}')

elif selection == 'Lineup Optimizer':
    st.header('Lineup Optimizer')
    st.write('This tool will recommend optimal starters based on projections.')
    st.info('Feature in development — loading logic coming soon.')

elif selection == 'Trade Finder':
    st.header('Trade Finder')
    st.write('Analyze trades based on player tiers and positional need.')
    st.success('Trade suggestion engine stub active.')

elif selection == 'Draft Pick Tracker':
    st.header('Draft Pick Tracker')
    st.write('View who owns which picks for future draft planning.')
    st.warning('Pick data will populate once synced with Sleeper.')

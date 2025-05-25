import streamlit as st

st.set_page_config(page_title='Dynasty Football Tool')

st.sidebar.title('Navigation')
selection = st.sidebar.radio('Go to', ['Dashboard', 'Lineup Optimizer', 'Trade Finder', 'Draft Pick Tracker'])

st.title('Dynasty Football Management MVP')

if selection == 'Dashboard':
    st.header('League Dashboard')
    st.write('Overview of your league, team summaries, and metrics.')

elif selection == 'Lineup Optimizer':
    st.header('Lineup Optimizer')
    st.write('Optimize your starting lineup based on projections (coming soon).')

elif selection == 'Trade Finder':
    st.header('Trade Finder')
    st.write('Suggests fair trades based on roster need and player value (coming soon).')

elif selection == 'Draft Pick Tracker':
    st.header('Draft Pick Tracker')
    st.write('Track who owns which picks and make smarter trades.')

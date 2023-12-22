import streamlit as st
import pandas as pd
import pickle

# Load the trained models
with open('pipe_T20.pkl', 'rb') as f:
    pipe_T20 = pickle.load(f)
with open('pipe_ODI.pkl', 'rb')as s:
    pipe_ODI = pickle.load(s)
with open('pipe_TEST.pkl', 'rb') as d:
    pipe_TEST = pickle.load(d)

# Define the teams and cities
teams = ['Australia', 'India', 'Bangladesh', 'New Zealand', 'South Africa', 'England','West Indies', 'Afghanistan',
         'Pakistan', 'Sri Lanka', 'Zimbabwe', 'Ireland']
cities = ['Dubai', 'Colombo', 'Harare', 'Johannesburg', 'Mirpur', 'kland', 'Cape Town', 'Abu Dhabi', 'Pallekele',
          'Sydney', 'Melbourne', 'Durban', 'London', 'Lahore', 'Nottingham', 'Hamilton', 'Centurion', 'Chittagong',
          'Dublin', 'Wellington', 'Hambantota', 'St Lucia', 'Chandigarh', 'Barbados', 'Mount Maunganui']


# Define the app
def app():
    # Set up the page
    st.title('Cricket Score Predictor')
    st.write('Select the type of match and input the current game state to predict the final score.')

    # Get the match type
    match_type = st.selectbox('Match type', ['T20', 'ODI', 'Test'])

    # Get the input values from the user
    col1, col2, col3 = st.columns(3)
    with col1:
        batting_team = st.selectbox('Batting team', teams)
    with col2:
        bowling_team = st.selectbox('Bowling team', teams)
    with col3:
        city = st.selectbox('City', cities)

    col1, col2, col3 = st.columns(3)
    with col1:
        current_score = st.number_input('Current score', min_value=0.0, step=0.1)
    with col2:
        overs_done = st.number_input('Overs done', min_value=0.0, step=0.1)
    with col3:
        wickets_out = st.number_input('Wickets out', min_value=0.0, max_value=10.0, step=0.1)

    last_five = st.number_input('Runs scored in last 5 overs', min_value=0.0, step=0.1)

    # Calculate the remaining balls and wickets
    if match_type == 'T20':
        balls_left = 120 - overs_done * 10
        wickets_left = 10 - wickets_out
    elif match_type == 'ODI':
        balls_left = 300 - overs_done * 10
        wickets_left = 10 - wickets_out
    else:
        balls_left = None
        wickets_left = None

    # Calculate the current run rate
    if overs_done > 0:
        current_run_rate = current_score / overs_done
    else:
        current_run_rate = None

    # Make the prediction
    if st.button('Predict_Score'):
        if match_type == 'T20':
            input_data = pd.DataFrame({
                'batting_team': [batting_team], 'bowling_team': [bowling_team], 'city': [city],
                'current_score': [current_score], 'current_run_rate': [current_run_rate],
                'wickets_left': [wickets_out], 'balls_left': [balls_left], 'last_five': [last_five]
            })
            result = pipe_T20.predict(input_data)
            st.header("Predicted Score - " + str(int(result[0])))

        elif match_type == 'ODI':
            input_data = pd.DataFrame({
                'batting_team': [batting_team], 'bowling_team': [bowling_team], 'city': [city],
                'current_score': [current_score], 'current_run_rate': [current_run_rate],
                'wickets_left': [wickets_left], 'balls_left': [balls_left], 'last_five': [last_five]
            })
            result = pipe_ODI.predict(input_data)
            st.header("Predicted Score - " + str(int(result[0])))
        elif match_type == 'TEST':
            input_data = pd.DataFrame({
                'batting_team': [batting_team], 'bowling_team': [bowling_team], 'city': [city],
                'current_score': [current_score], 'current_run_rate': [current_run_rate],
                'wickets_left': [wickets_left], 'balls_left': [balls_left], 'last_five': [last_five]
            })
            result = pipe_TEST.predict(input_data)
            st.header("Predicted Score - " + str(int(result[0])))


def app2():
    return None
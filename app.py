
import pandas as pd
import streamlit as st
st.beta_set_page_config(page_title = "Portfolio Analytics", page_icon="💸")

from datetime import date, timedelta
from rest_api.fetch_data import (get_symbol_data)
from visualizations.plots import (
    beta,
    basic_portfolio,
    portfolio_pie,
    display_portfolio_return,
    display_heat_map,
    monte_carlo
)


def load_heading():
    """The function that displays the heading.
        Provides instructions to the user
    """
    with st.container():
        
        st.title('Alihan Ucar Portfolio Tracker')
        header = st.subheader('This App performs historical portfolio analysis and future analysis with Monte Carlo Simulation')
        st.subheader('Asset Allocation')
        st.text('This application has been forked and modified by alihanucar for personal use but it was originally developed by the GitHub user Analitico-771')


def get_choices():
    """Prompts the dialog to get the All Choices.

    Returns:
        An object of choices and an object of combined dataframes.
    """
    choices = {}
    user_start_date = date.today()
    yesterday = user_start_date - timedelta(days=1)

    # add_selectbox = st.sidebar.selectbox(
    # "How would you like to be contacted?",
    # ("Email", "Home phone", "Mobile phone")
    # )
    
    warning_1 = st.sidebar.write("Max yrs you should go back is 5!")
    years_back = st.sidebar.number_input('How Many Years Back From Today?', min_value=1, max_value=5, value=1)

    #warning_2 = st.sidebar.write("You must enter 1 Index such as SPY, 3 Stock, and 2 Crypto Symbol names. Please refer to Yahoo Finance for a list of applicable ticker symbols.  Type the symbol EXACTLY as provided by Yahoo Finance.")
        
    tickers = ('SPY,SOXX,IVV,DBE')

    crypto_symbols = ('BTC-USD,ETH-USD,AVAX-USD')
    # 'SPY,SOXX,IVV,DBE,BTC-USD,ETH-USD, AVAX-USD'

    # Set the weights
    weights_str = ('0.0,0.2,0.45,0.1,0.05,0.10,0.10')
    # Set Initial Investment
    investment = (1000)
    # Set the investment forecast_years
    forecast_years = st.sidebar.number_input('Enter The Forecast Years For The Simulation', min_value=5, max_value=15, value=5)
    # Set the number of simulations to run_years
    st.sidebar.write("We recommend you run 500 sim runs. 250 is minimum and 1000 is max")
    sim_runs = st.sidebar.number_input('Enter The Number Of Simulations To Run', min_value=250, max_value=1000, value=250)

    # Set the start_date to years_back  
    start_date = user_start_date.replace(year=(yesterday.year - years_back), month=yesterday.month, day=yesterday.day)
    # Set the end_date to yesterday
    end_date = yesterday

    # Every form must have a submit button.
    submitted = st.sidebar.button("Submit")

    symbols = []
    reset = False

    # Reusable Error Button DRY!
    def reset_app(error):
        st.sidebar.write(f"{error}!")
        st.sidebar.write(f"Check The Syntax")
        reset = st.sidebar.button("RESET APP")

    if submitted:
        # convert  strings to lists
        tickers_list = tickers.split(",")
        weights_list = weights_str.split(",")
        crypto_symbols_list = crypto_symbols.split(",")
        # Create the Symbols List
        symbols.extend(tickers_list)
        symbols.extend(crypto_symbols_list)
        # Convert Weights To Decimals
        weights = []
        for item in weights_list:
            weights.append(float(item))

        # CheckThe User Input
        #if len(tickers_list) != 4:
            #reset_app('Check Stock Tickers')
        #if len(crypto_symbols_list) != 2:
            #reset_app('Check Crypto Tickers')
        #if sum(weights) != 1:
            #reset_app('Check Weights')

        #if reset:
            # Clears all singleton caches:
            #tickers = ('SPY,AMZN,TSLA,NVDA')
            #crypto_symbols = ('BTC-USD,ETH-USD')
            #weights_str = ('0.2,0.2,0.25,0.1,0.05,0.10,0.10')
            #st.experimental_singleton.clear()

        else:    
            # Submit an object with choices
            choices = {
                'user_start_date': user_start_date,
                'start_date': start_date,
                'end_date': end_date,
                'symbols': symbols,
                'weights': weights,
                'investment': investment,
                'forecast_years': forecast_years,
                'sim_runs': sim_runs
            }
            # Load combined_df
            combined_df = get_symbol_data(choices)
            # return object of objects
            return {
                'choices': choices,
                'combined_df': combined_df
            }


def run():
    """The main function for running the script."""

    load_heading()
    choices = get_choices()
    if choices:
        portfolio_pie(choices['choices'])     
        beta(choices['combined_df'])
        basic_portfolio(choices['combined_df'])
        display_heat_map(choices['combined_df'])
        display_portfolio_return(choices['combined_df'], choices['choices'])
        with st.spinner('Running Monte Carlo Simulation...'):
            monte_carlo(choices['combined_df'], choices['choices'])


if __name__ == "__main__":
    run()

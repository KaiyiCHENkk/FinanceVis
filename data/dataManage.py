import pandas as pd

# load the investment data
def load_investment_data():
    df = pd.read_csv('data\Investment Transaction.csv')
    df['Transaction Date'] = pd.to_datetime(df['Transaction Date'], dayfirst=True)
    df['Month_Year'] = df['Transaction Date'].dt.strftime('%Y-%m')
    return df

# filter the buy and sell actions according to account number
def filter_buysell_data(df, account_number, transaction_type):
    action = 'Market buy' if transaction_type == 'buy' else 'Market sell'
    if account_number == 9:
        filtered_df = df[df['Action'].str.contains(action)]
    else:
        filtered_df = df[(df['Account Number'] == account_number) & (df['Action'].str.contains(action))]
    return filtered_df

# aggregate data by month and number of shares
def aggregate_data_volume(filtered_df):
    return filtered_df.groupby('Month_Year')['No. of shares'].sum()

# aggregate data by month and Total value
def aggregate_data_value(filtered_df):
    return filtered_df.groupby('Month_Year')['Total (GBP)'].sum()

# filter the dividend data
def filter_dividend_data(df):
    dividend_types = [
        "Dividend (Ordinary)",
        "Dividend (Dividend)",
        "Dividend (Demerger)",
        "Dividend (Bonus)",
        "Dividend (Ordinary manufactured payment)",
        "Dividend (Dividends paid by us corporations)",
        "Dividend (Dividends paid by foreign corporations)"
    ]
    return df[df['Action'].isin(dividend_types)]

# Sum up 'Total (GBP)' for each 'Ticker' and 'Type of Dividend'
def aggregate_dividend_data(filtered_df):
    aggregated_df = filtered_df.groupby(['Ticker', 'Action'])['Total (GBP)'].sum().unstack().fillna(0)
    return aggregated_df

# Sum up 'Total (GBP)' for each 'Ticker' and 'Type of Dividend' by month
def aggregate_dividend_data_by_month(filtered_df):
    return filtered_df.groupby(['Month_Year', 'Ticker', 'Action'])['Total (GBP)'].sum().reset_index()





# Load stock close price data
def load_stock_close_data():
    df = pd.read_csv('data/API.csv', index_col='Date')
    return df

# load time range of each stock
def load_investment_dates():
    df = pd.read_csv('data/stock_time.csv', parse_dates=['Start Date','End Date'], dayfirst=True)
    return df


# load the data for each stock for single or compare view
def load_ticker_stock_data(ticker):
    file_path = f'data/{ticker}_stock_data.csv'
    df = pd.read_csv(file_path, parse_dates=['Date'], dayfirst=True)
    return df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]

# get all the tickers in the user dataset
def get_all_tickers():
    df = pd.read_csv('data/stock_time.csv')
    return df['Ticker'].unique()






# def load_company_data():
#     df = pd.read_csv('data/Investment Company.csv')
#     ticker_order = {ticker: i for i, ticker in enumerate(df['Ticker Symbol'].unique(), start=1)}
#     df['Ticker Symbol Index'] = df['Ticker Symbol'].map(ticker_order)
#     return df


def load_company_data():
    df = pd.read_csv('data/Investment Company.csv')
    return df




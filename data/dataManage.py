import pandas as pd

# load the investment data
def load_investment_data():
    """
    Load investment transactions from a CSV file and process dates.

    Returns:
        DataFrame: A pandas DataFrame with the investment transactions, including
                   parsed and formatted transaction dates and a new 'Month_Year' column.
    """

    df = pd.read_csv('data\Investment Transaction.csv')
    df['Transaction Date'] = pd.to_datetime(df['Transaction Date'], dayfirst=True)
    df['Month_Year'] = df['Transaction Date'].dt.strftime('%Y-%m')
    return df

# filter the buy and sell actions according to account number
def filter_buysell_data(df, account_number, transaction_type):
    """
    Filters buy and sell actions based on account number and transaction type.

    Parameters:
        df (DataFrame): The DataFrame containing transaction data.
        account_number (int): The account number to filter by.
        transaction_type (str): 'buy' or 'sell' indicating the type of transaction.

    Returns:
        DataFrame: A filtered DataFrame based on the specified action and account number.
    """
    
    action = 'Market buy' if transaction_type == 'buy' else 'Market sell'
    if account_number == 9:
        filtered_df = df[df['Action'].str.contains(action)]
    else:
        filtered_df = df[(df['Account Number'] == account_number) & (df['Action'].str.contains(action))]
    return filtered_df

# aggregate data by month and number of shares
def aggregate_data_volume(filtered_df):
    """
    Aggregates the volume of shares by month.

    Parameters:
        filtered_df (DataFrame): The DataFrame filtered for specific transaction types.

    Returns:
        Series: A pandas Series aggregating the number of shares per month.
    """
    
    return filtered_df.groupby('Month_Year')['No. of shares'].sum()

# aggregate data by month and Total value
def aggregate_data_value(filtered_df):
    """
    Aggregates the total value of transactions by month.

    Parameters:
        filtered_df (DataFrame): The DataFrame filtered for specific transaction types.

    Returns:
        Series: A pandas Series aggregating the total value in GBP per month.
    """
    
    return filtered_df.groupby('Month_Year')['Total (GBP)'].sum()

# filter the dividend data
def filter_dividend_data(df):
    """
    Filters out the dividend data from transaction data.

    Parameters:
        df (DataFrame): The DataFrame containing transaction data.

    Returns:
        DataFrame: A DataFrame containing only the rows with dividend transactions.
    """
    
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
    """
    Summarizes the total GBP of dividends by ticker and type.

    Parameters:
        filtered_df (DataFrame): The DataFrame containing filtered dividend transactions.

    Returns:
        DataFrame: An aggregated DataFrame with total GBP summed up for each ticker and dividend type.
    """

    aggregated_df = filtered_df.groupby(['Ticker', 'Action'])['Total (GBP)'].sum().unstack().fillna(0)
    return aggregated_df

# Sum up 'Total (GBP)' for each 'Ticker' and 'Type of Dividend' by month
def aggregate_dividend_data_by_month(filtered_df):
    """
    Aggregates dividend data by month, ticker, and type.

    Parameters:
        filtered_df (DataFrame): The DataFrame containing filtered dividend transactions.

    Returns:
        DataFrame: An aggregated DataFrame with total GBP summarized by month, ticker, and type.
    """

    return filtered_df.groupby(['Month_Year', 'Ticker', 'Action'])['Total (GBP)'].sum().reset_index()

# Load stock close price data for single view
def load_stock_close_single():
    """
    Loads daily closing prices of stocks.

    Returns:
        DataFrame: A DataFrame with the daily stock close price data including a parsed Date column.
    """
    df = pd.read_csv('data/API.csv', dtype={'Date': 'object'})
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', dayfirst=True)
    
    return df

# Load stock close price data
def load_stock_close_data():
    """
    Loads daily closing prices of stocks indexed by date.

    Returns:
        DataFrame: A DataFrame with the daily stock close price data, indexed by date.
    """
    df = pd.read_csv('data/API.csv', index_col='Date')
    return df

# load time range of each stock
def load_investment_dates():
    """
    Loads the start and end dates for investments.

    Returns:
        DataFrame: A DataFrame with the start and end dates of stocks parsed as date types.
    """
    df = pd.read_csv('data/stock_time.csv', parse_dates=['Start Date','End Date'], dayfirst=True)
    return df

# load the data for each stock for single or compare view
def load_ticker_stock_data(ticker):
    """
    Loads stock data for a specific ticker.

    Parameters:
        ticker (str): The stock ticker symbol.

    Returns:
        DataFrame: A DataFrame containing the stock data for the specified ticker, including parsed dates.
    """
    file_path = f'data/{ticker}_stock_data.csv'
    df = pd.read_csv(file_path, parse_dates=['Date'], dayfirst=True)
    return df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]

# get all the tickers in the user dataset
def get_all_tickers():
    """
    Retrieves all stock ticker symbols from the dataset.

    Returns:
        ndarray: An array of unique ticker symbols.
    """
    df = pd.read_csv('data/stock_time.csv')
    return df['Ticker'].unique()

def load_company_data():
    """
    Loads data for investment companies.

    Returns:
        DataFrame: A DataFrame containing data about investment companies.
    """
    df = pd.read_csv('data/Investment Company.csv')
    return df


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def read_data():
	"""
	Read in the datasets and join them together to make a single data frame
	"""
	df_18 = pd.read_csv("./pp-2018.csv", header=None)
	df_19 = pd.read_csv("./pp-2019.csv", header=None)
	df_20 = pd.read_csv("./pp-2020.csv", header=None)

	df = pd.concat([df_18, df_19, df_20])

	labels = ['ID', 'Price', 'Date', 'Postcode', 'PropertyType', 'Old_New',
	              'Duration', 'PAON', 'SAON', 'Street', 'Locality', 'Town_City', 
	              'District', 'County', 'PPD_type', 'Record_status']
	df.columns = labels

	# replace nans with None string
	df = df.replace(np.nan, 'None', regex=True)

	return df



def highest_price_by_county(df):
    """
    Returns the highest prices within each county
    """
    # group the dataframe by County
    grouped_df = df.groupby(['County'])
    # use the transform method to find the maximum price for each county
    maximum_prices = grouped_df['Price'].transform(max)
    # find the indexes of the rows with the maximum prices
    maximum_prices_idxs = maximum_prices == df['Price']
    # return the dataframe, sorted by highest to lowest price
    return df[maximum_prices_idxs].sort_values('Price', ascending=False)



def top_5_by_quarter(df):
    """
    Returns the top 5 postcodes districts within each quarter.
    I couldn't find a way to display the data as a data frame, so instead
    I've simply used 2 loops and printed the results.
    """
    # define postcode district (split and take string before space)
    df['Postcode_district'] = df['Postcode'].apply(lambda x: x.split()[0])
    # split the date into the year and month
    df['Year'] = df['Date'].str[:4].astype(int)
    df['Month'] = df['Date'].str[5:7].astype(int)
    # use the cut method to assign each row a quarter
    bins = [0,3,6,9,12]
    quarter_labels = ['Q1', 'Q2', 'Q3', 'Q4']
    df['Quarter'] = pd.cut(df['Month'], bins, labels=quarter_labels)
    # group the dataframe by year and quarter, and then find the 5 largest prices (can't get this to work)
#     grouped_df = df.groupby(['Year', 'Quarter'])['Price'].nlargest(5)
#     return grouped_df
    for year in [2018, 2019, 2020]:
        for quarter in ['Q1', 'Q2', 'Q3', 'Q4']:
            temp_df = x[(x.Year == year) & (x.Quarter == quarter)][['Postcode_district', 'Price']]
            print(year, quarter)
            print(temp_df.nlargest(5, 'Price'))
            print("")



def transaction_value_concentration(df):
    """
    Should return percentage of transactions. 
    I think a pivot table will be needed to set year as index and property type as column.
    However, I couldn't find a correct solution.
    """
    return df.pivot_table(index='Year', columns='PropertyType', values='Price', aggfunc='mean')



def volume_and_median_price_comp(df1, df2):
    """
    Takes 2 data frames and returns a single data frame showing the median and 
    percentage differences between them, grouped by price ranges.
    """
    # Create bins and cut the data for both data frames
    bins = [0,250000,500000,750000,1000000,2000000,5000000,np.inf]
    for df in [df1, df2]:
        df['Price_bin'] = pd.cut(df['Price'], bins)
    # Group the dataframes based on the price bins. Save the median and counts in the bins.
    df1 = df1[['Price', 'Price_bin']].groupby('Price_bin').agg(['median', 'count'])
    df2 = df2[['Price', 'Price_bin']].groupby('Price_bin').agg(['median', 'count'])
    # Create new dataframe and find the percentage differences
    df_temp = pd.DataFrame()
    df_temp['Volume_change'] = 100.0 * (df1[('Price', 'count')] - df2[('Price', 'count')]) / df2[('Price', 'count')]
    df_temp['Median_change'] = 100.0 * (df1[('Price', 'median')] - df2[('Price', 'median')]) / df2[('Price', 'median')]
    return df_temp



def property_returns():
    """
    I imagine the method would be something like:
        1) Find all duplicate addresses in the data frame using something like df.duplicated
        2) Record the amount of time between successive addresses and take the average
        3) Group by year and holding type, and find the change in value between successive values
    """
    pass
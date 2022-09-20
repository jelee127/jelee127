import pandas as pd 

# Function 1  Driver - Bryan
# Takes in 3 filenames  
# loads in the files
# For each file, load the contents of the file to a dataframe
# There are 3 files so we will make three dataframe
# return tuple with 3 dataframes
def load_files():

    nba_df = pd.read_csv('NBA_data.csv')
    nfl_df = pd.read_csv('NFL_data.csv')
    mlb_df = pd.read_csv('MLB_data.csv')

 
    #Add a new column so we knw the affliation of the player (MLB, NBA , OR NFL)
    nba_df['Affliation'] = 'NBA'
    nfl_df['Affliation'] = 'NFL'
    mlb_df['Affliation'] = 'MLB'
    
    nfl_df = clean_data(nfl_df)
    
    #print(nfl_df.head())
    
    return (nba_df[['Name', 'Salary', 'Affliation']], 
            nfl_df[['Name', 'Salary', 'Affliation']], 
            mlb_df[['Name', 'Salary', 'Affliation']])

#load_files()

# Function 2  Driver - Bryan
# Takes in a dataframe
# Clean the NFL dataframe since it has unwanted values in that data file
def clean_data(df):
    
    
    cleaned_list = []
    #Clean NFL data of commas and dollar signs
        #https://pandas.pydata.org/pandas-docs/stable/user_guide/text.html
    df['Salary'] = df['Salary'].str.replace('$', '')
    df['Salary'] = df['Salary'].str.replace(',', '')
    df['Salary'] = df['Salary'].str.strip() 
    
    #Purpose of the for loop below is to clean the data in "Names" column
    #Most efficient way to loop through a dataframe
        #https://stackoverflow.com/questions/7837722/what-is-the-most-efficient-way-to-loop-through-dataframes-with-pandas
    for index, row in df.iterrows():
        
       split_word = df.at[index, 'Name'].split("\\")
       cleaned_list.append(split_word[0])
    
     
    df['Name'] =  cleaned_list  
    
    return df 


# Function 2  Driver - Bryan
# Takes in a tuple filled with dataframes --> (dataframes1, dataframes2, dataframes3)
# Finds the top highest players out of all the files
# First find the top 10 players of each file first 
    # Take the first top 10 players from the dictionary
# Merge all the top 10 players from each dataframe

def find_top_10(df_tuple):
    
    nba_df = df_tuple[0]
    nfl_df = df_tuple[1]
    mlb_df = df_tuple[2]
    
    #Have to convert columns to same values or will get a value error
        #https://stackoverflow.com/questions/50649853/trying-to-merge-2-dataframes-but-get-valueerror
    
    nba_df['Salary'] = nba_df['Salary'].astype(float)
    mlb_df['Salary'] = mlb_df['Salary'].astype(float)
    nfl_df['Salary'] = nfl_df['Salary'].astype(float)
    
    nba_top = nba_df.iloc[0:10]
    nfl_top = nfl_df.iloc[0:10]
    mlb_top = mlb_df.iloc[0:10]
 
    merge_data = nba_top
    
    #Have to merge twice because pandas can only merge 2 frames at a time

    merge_data = merge_data.merge(nfl_top, 
        on = ['Name', "Salary" , 'Affliation'], how = "outer")
    
    merge_data = merge_data.merge(mlb_top, 
        on = ['Name', "Salary" , 'Affliation'], how = "outer")
    
    
    #Sort Values method referenced from:
        #https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html
    merge_data = merge_data.sort_values(by = ['Salary'], ascending = False)
    
    #print(merge_data.head(10))
    
    return merge_data.head(10)
     
find_top_10(load_files()) 

# Function 3 Driver - Bryan 
# Takes in a tuple of dataframes
# Search function for people
# Ask user for player and their affiliation 
# return a dataframe entry

# Function 4 Driver - Bryan 
# Takes in a dataframe
# Displays a barchart for the top 10 players
# return none 

# Function 5
# Input validation and format
# Takes in a
# Check to see if user enters a valid value
# Inform user if they enter a value that is not found
    #Ex: If they enter a nonexistent player tell them that
# Continually ask the user until they enter a valid
# returns none


# Function 6 Driver - Bryan 
# Takes in a dataframe
# Displays a barchart for each a player searches for
# returns none

# Function 7
# Takes in a tuple pf dataframes
# Calculate the 5 number summary for all 3 dataframes
# Print out the 5 number summaries


# Function 8
# Takes in a dataframe entry of a player and a tuple of dataframes
# Merge all dataframes into one dataframe
# Calculate the percentile of the player
    # Find the standard deviation
    # Find the mean of all players
    # use this information to calculate z score
    # use a python function that calculates z score probability
# Print out the percentile


# Main Function 
# Run the program
# Continually loop and ask user for info until user types "no"
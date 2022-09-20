import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import statistics
import scipy.stats as st


# Function 1  Driver - Bryan, Navigator - JaeEun
# Takes in 3 filenames  
# loads in the files
# For each file, load the contents of the file to a dataframe
# There are 3 files so we will make three dataframe
# return tuple with 3 dataframes
def load_files():

    #read in all data
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

# Function 2  Driver - Bryan, Navigator - JaeEun
# Takes in a dataframe
# Clean the NFL dataframe since it has unwanted values in that data file
def clean_data(df):
    
    
    cleaned_list = []
    #Clean NFL data of commas and dollar signs
        #https://pandas.pydata.org/pandas-docs/stable/user_guide/text.html
    df['Salary'] = df['Salary'].str.replace('$', '')
    df['Salary'] = df['Salary'].str.replace(',', '')
    df['Salary'] = df['Salary'].str.strip() 
    
    #Have to convert columns to same values or will get a value error
        #https://stackoverflow.com/questions/50649853/trying-to-merge-2-dataframes-but-get-valueerror
    df['Salary'] = df['Salary'].astype(float)
    
    #Purpose of the for loop below is to clean the data in "Names" column
    #Most efficient way to loop through a dataframe
        #https://stackoverflow.com/questions/7837722/what-is-the-most-efficient-way-to-loop-through-dataframes-with-pandas
    for index, row in df.iterrows():
        
       split_word = df.at[index, 'Name'].split("\\")
       cleaned_list.append(split_word[0])
    
     
    df['Name'] =  cleaned_list  
    
    return df 


# Function 2  Driver - Bryan, Navigator - David
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

 
# Function 3 Driver - Bryan, Navigator - JaeEun 
# Takes in a tuple of dataframes
# Search function for people
# Ask user for player and their affiliation 
# return a tuple with  name, salary and affiliation 

def search_player(df_tuple, player, affiliation):
    
    affiliation = affiliation.upper()
    nba_df = df_tuple[0]
    nfl_df = df_tuple[1]
    mlb_df = df_tuple[2]
    
    find_player = ''
    
    #check the affiliation so we can look at the right file
    if affiliation == 'NBA':
        find_player = nba_df
    
    elif affiliation == 'NFL':
        find_player = nfl_df
    
    elif affiliation == 'MLB':
        find_player = mlb_df
        
    salary = 0
    
    
    if len(find_player[find_player['Name'] == player]) > 0 :
        
         #Referenced from https://stackoverflow.com/questions/21800169/python-pandas-get-index-of-rows-which-column-matches-certain-value
         #Find an index of a found value
    
         row = find_player.index[find_player['Name'] ==  player]
    
         
         #clean up data to make it to float
         try:
            salary = find_player.iloc[row]['Salary']
            salary = str(salary)
            salary = (salary[2:]).strip()
            #print('THE SALARY IS: ' ,  str(salary))
            salary = float((salary).split('\n')[0])
         except ValueError:
            
            salary = salary.strip()
            salary = float((salary).split()[1])
            #print('THE SALARY IS: ' ,  str(salary))
            
         except:
            
            print('Sorry we have the player, but the data on the player cannot be displayed')
        
            
         #print('THE SALARY IS: ' ,  str(salary))
         
         
    else:
        
        print('The player is not in the list')
   
    return (player,  salary, affiliation)



# Function 4 Driver - Bryan, Navigator - David
# Takes in a dataframe
# Displays a color coded barchart for the top 10 players
# return none 
def plot_top_10(df):  
    
    colors = []
    
    #color changes with each affiliation
    for affil in df['Affliation']:
        
        if affil == 'NBA':
            
            colors.append('red')
              
        elif affil == 'NFL':
        
            colors.append('green')
            
        elif affil == 'MLB':
        
            colors.append('blue')
            
         
    #refernced from: https://matplotlib.org/3.1.0/api/_as_gen/matplotlib.pyplot.bar.html
    x = df['Name']
    y = df['Salary']
    
    width = .35
    
    fig = plt.figure(figsize=(13, 5))
    labels = plt.bar(x, y, color = colors)
    
    #refernced from:
        #https://stackoverflow.com/questions/34001751/python-how-to-increase-reduce-the-fontsize-of-x-and-y-tick-labels
    plt.tick_params(axis="x", labelsize= 7)
    plt.tick_params(axis="y", labelsize= 7)
    
    #fontsize refrenced from
        #https://stackoverflow.com/questions/712082/barchart-sizing-of-text-barwidth-with-matplotlib-python
    plt.ylabel('Salaries (USD)', fontsize = 15)
    plt.xlabel('Names', fontsize = 15) 
    
    plt.title('Ten highest base salaries in the NBA, NFL, and MLB', fontsize = 20)
    
    #referenced from: https://matplotlib.org/3.1.0/tutorials/intermediate/legend_guide.html
    NBA_patch = mpatches.Patch(color='red', label='NBA')
    NFL_patch = mpatches.Patch(color='green', label='NFL')
    MLB_patch = mpatches.Patch(color='blue', label='MLB')
    
    autolabel_1(labels, plt)
        
    plt.legend(handles=[NBA_patch, NFL_patch, MLB_patch])
   
    plt.show()
    
#Source of this function https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/barchart.html
def autolabel_1(rects, plt):
    """Attach a text label above each bar in *rects*, displaying its height."""
    
    for rect in rects:
        height = rect.get_height()
        plt.annotate('${:,}'.format(height), # just add a + and the percentile you want
                    xy= (rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize= 8)
       


#Source of this function https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/barchart.html
#modified this function to fit our needs
def autolabel(rects, plt, percentile):
    """Attach a text label above each bar in *rects*, displaying its height."""
    count = 0
    
    for rect in rects:
        height = rect.get_height()
        formatted_salary =   '${:,}'.format(height) + " "
        formatted_percentile =  " (" + str(round(percentile[count], 4)) + "th percentile"  + ")"
        plt.annotate(formatted_salary  +  formatted_percentile, # just add a + and the percentile you want
                    xy= (rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize= 8)
        count += 1
        
        
    
# Function 5 Driver - JaeEun, Navigator - Bryan
# Input validation and format
# Takes in a value
# Check to see if user enters a valid value
# Inform user if they enter a value that is not found
    #Ex: If they enter a nonexistent player tell them that
# Continually ask the user until they enter a valid
# returns none


# Function 6 Driver - Bryan, Navigator - JaeEun
# Takes in a dataframe
# Displays a barchart for each a player searches for
# returns none
def plot_searched_players(df, player_names, player_affils):
    
    # makes lists to store our data
    name_list = []
    salary_list = []
    affiliaton_list = []
    percentile_list = []
    colors = []
    indices = []
    
    count = 0
    
    #for loop adds elements to lists
    for name in player_names:
        
        files = load_files()
        
        player_tuple = search_player(files, 
                                     player_names[count], 
                                     player_affils[count])
        
        percentile = create_player_perc(files, player_tuple[0], player_tuple[2])
        
        percentile_list.append(percentile)
        name_list.append(player_tuple[0])
        salary_list.append(player_tuple[1])
        affiliaton_list.append(player_tuple[2])
        
        if affiliaton_list[count] == 'NBA':
        
             colors.append('red')
            
        elif  affiliaton_list[count] == 'NFL':
        
            colors.append('green')
            
        elif  affiliaton_list[count] == 'MLB':
        
            colors.append('blue')
            
        indices.append(count)
        count += 1
     
        #print(name_list)
        #print(salary_list)
        #print(colors)

    #all code below is used to create a fully label bar chart
    
    #referenced from: https://matplotlib.org/3.1.0/api/_as_gen/matplotlib.pyplot.bar.html
   
    plt.figure(figsize=(10, 5))
    
    labels = plt.bar(name_list, salary_list, color = colors)
    
    #referenced from:
        #https://stackoverflow.com/questions/34001751/python-how-to-increase-reduce-the-fontsize-of-x-and-y-tick-labels
    plt.tick_params(axis="x", labelsize= 7)
    plt.tick_params(axis="y", labelsize= 7)
    
    #fontsize refrenced from
        #https://stackoverflow.com/questions/712082/barchart-sizing-of-text-barwidth-with-matplotlib-python
    
    plt.ylabel('Salaries(USD)', fontsize = 15)
    plt.xlabel('Player Names', fontsize = 15)
    plt.suptitle('Your searched Players', fontsize = 20)
     
    #referenced from: https://matplotlib.org/3.1.0/tutorials/intermediate/legend_guide.html
    NBA_patch = mpatches.Patch(color='red', label='NBA')
    NFL_patch = mpatches.Patch(color='green', label='NFL')
    MLB_patch = mpatches.Patch(color='blue', label='MLB')
    
    
    autolabel(labels, plt, percentile_list)
    
    plt.legend(handles=[NBA_patch, NFL_patch, MLB_patch])
    plt.show()



# Function 7 Driver - David, Navigator - Bryan 
# Takes in a tuple pd dataframes
# Calculate the 5 number summary for all 3 dataframes
# Print out the 5 number summaries

def create_fns(dfs):
    
    x, y, z = dfs
    nba_fns = x.describe()
    nfl_fns = y.describe()
    mlb_fns = z.describe()
    
     
    merge_data = x.merge(y, 
        on = ['Name', "Salary" , 'Affliation'], how = "outer")
    
    merge_data = merge_data.merge(x, 
        on = ['Name', "Salary" , 'Affliation'], how = "outer")
    
    all_data_fns = merge_data.describe()
    
    #Have to convert columns to same values or will get a value error
    #https://stackoverflow.com/questions/50649853/trying-to-merge-2-dataframes-but-get-valueerror
    
    nba = nba_fns['Salary'][3:].astype(str)  
    nfl = nfl_fns['Salary'][3:].astype(str)  
    mlb  = mlb_fns['Salary'][3:].astype(str)  
    
    print()
    print("NBA")
    print(nba)
    
    print()
    print("NFL")
    print(nfl)
    
    print()
    print("MLB")
    print(mlb)
    
# Function 8 Driver - David, Navigator - Bryan
# Takes in a dataframe entry of a player and a tuple of dataframes
# Merge all dataframes into one dataframe
# Calculate the percentile of the player
    # Find the standard deviation
    # Find the mean of all players
    # use this information to calculate z score
    # use a python function that calculates z score probability
# Return the percentile
def create_player_perc(dfs, name, affiliation):
    
    #load info to dataframes
    nba, nfl, mlb = dfs
    
    name, salary, affil = search_player(dfs, name, affiliation)
    
    nba = nba.merge(nfl, on = ['Name', "Salary" , 'Affliation'], how='outer' )

    all_df = nba.merge(mlb, on = ['Name', "Salary" , 'Affliation'], how='outer')
    
    #get the standard deviation
    collective_stdev = all_df.std()
    #print("STDEV IS ", collective_stdev.values)

    #get the mean
    collective_mean = all_df.mean()
    #print("MEAN IS ", (collective_mean.values)[0])

    # calculate the z score percentile
    z_score = (salary - collective_mean[0]) / collective_stdev[0]
    percentile = st.norm.cdf(z_score)
    percentile *= 100
    #print("{} is in the {} percentile.".format(name, percentile))
    
    return percentile
         
    

# Main Function Driver - JaeEun, Navigator - David
# Run the program
# Continually loop and ask user for info until user types "no"
if __name__ ==  "__main__":
    
    names_list = []
    affil_list = []
    
    #create_fns(load_files())
    create_player_perc(load_files(), "Tom Brady", "NFL")
    
    plot_top_10(find_top_10(load_files()))
   
    #continually loop until user types quit
    while True:
        
        #ask for user input
        get_player_name = input('Enter a player name (first name and last name): ')
        get_player_affil = input('Enter the player affiliation: ')
         
        #append to list user input
        names_list.append(get_player_name)
        affil_list.append(get_player_affil)
    
        #display bar chart for searched players
        plot_searched_players(load_files(),  names_list, affil_list)
        
        continue_search = input("type 'quit' to quit ")
        
        #check if user types in quit
        if (continue_search.lower() == 'quit'):
            
            break
        
   
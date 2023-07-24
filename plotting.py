import arabic_reshaper
from bidi.algorithm import get_display
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap


def plot_histogram_bycount(df,column,title=None,figsize=(10,10),threshold=0 ):

    '''
    plot a histogram given the dataframe and the column upon which we will plot the histogram 
    threshold is identified to plot any value with greater than or equal to that threshold to avoid sparse values in 
    our plot
    '''
    # Calculate the frequencies of each unique value in the column
    frequencies = df[column].value_counts()
    frequencies = frequencies[frequencies >= threshold]

    # Sort the frequencies in descending order
    sorted_frequencies = frequencies.sort_values(ascending=False)


    # Create a figure and axis
    fig, ax = plt.subplots(figsize=figsize)

    # Set the background color to black
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    # Set the axis label and tick colors to white
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    x=[]
    for item in sorted_frequencies.index:
        x.append(get_display(arabic_reshaper.reshape(item)))
        
    # Plot the sorted frequencies as a bar plot with the specified bar color and white edges
    ax.bar(x, sorted_frequencies.values, color='#44c2b1', edgecolor='white', linewidth=1.5)

    # Add value labels to the top of each bar
    for i, value in enumerate(sorted_frequencies.values):
        x =i
        y = value
        percentage = f'{y }'
        label = f'{percentage}'
        ax.text(x, y, label, ha='center', va='bottom', color='white',fontsize=10)

    # Rotate the x-axis labels by 90 degrees
    plt.xticks(rotation=90)
    
    if title:
        ax.set_title(title, color='white')
    # Show the plot
    plt.show()





def plot_linegraph(df,col,title):
    # Group the data by hour and count the number of posts in each hour
    hourly_counts = df.groupby(col).size()

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))

    # Set the background color to black
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    # Set the axis label and tick colors to white
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    # Plot the line plot with the specified line color and marker
    plt.plot(hourly_counts.index, hourly_counts.values, marker='o', color='#44c2b1', linewidth=2)

    plt.xlabel('Hour of the Day', color='white')
    plt.ylabel('Number of Stories', color='white')
    plt.title(title, color='white')
    plt.xticks(range(24))

    # Set the grid style to 'whitegrid' and disable vertical grid lines
    plt.grid(axis='y', color='white', linestyle='-')

    # Show the plot
    plt.show()


  

def plot_stackedbar(df, col1, col2, threshold):

    # Assuming you have a DataFrame 'df' containing the author names in 'author' column and the topics in 'topic' column

    # Group the data by col1 & col2 and count the occurrences of each topic for each author
    grouped_data = df.groupby([col1, col2]).size().reset_index(name='count')

    # Pivot the data to create a table with col1 as rows, col2 as columns, and 'count' as values
    pivot_table = grouped_data.pivot_table(index=col1, columns=col2, values='count', fill_value=0)

    # Calculate the total count of posts for each author
    author_post_counts = pivot_table.sum(axis=1)

    # Filter the authors based on the threshold
    popularity = author_post_counts[author_post_counts >= threshold]

    # Filter the pivot table to include only popular authors
    pivot_table_filtered = pivot_table.loc[popularity.index]

    # Normalize the values in the pivot table to show proportions instead of counts
    pivot_table_normalized = pivot_table_filtered.div(pivot_table_filtered.sum(axis=1), axis=0)

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))

    # Set the background color to black
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    # Set the axis label and tick colors to white
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    # Reshape the labels in col1 using arabic_reshaper and bidi algorithm
    x_labels = [get_display(arabic_reshaper.reshape(label)) for label in pivot_table_normalized.index]

    # Create the stacked bar plot with the 'deep' color palette from Seaborn
    sns.set_palette('deep')
    pivot_table_normalized.plot(kind='bar', stacked=True, ax=ax)

    # Set the x-axis labels
    plt.xticks(range(len(x_labels)), x_labels, rotation=90, ha='center', fontsize=10)

    plt.xlabel('Author', color='white')
    plt.ylabel('Proportion', color='white')
    plt.title('Proportion of Topics for Popular Authors (Post Counts >= '+ str(threshold) +')', color='white')

    # Show the plot
    plt.legend(title='Topic', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()




def plot_histogram_byavg(df,col1,col2, title=None, figsize=(7, 7)):
    '''
    Plot a histogram given the DataFrame and the column upon which we will plot the histogram.
    Threshold is identified to plot any value with greater than or equal to that threshold to avoid sparse values in our plot.
    '''
    # Calculate the average length of the story for each topic
    avg_story_length = df.groupby(col1)[col2].apply(lambda x: sum(len(story) for story in x) / len(x))
    
    # Sort the average story lengths in descending order
    sorted_avg_lengths = avg_story_length.sort_values(ascending=False)

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=figsize)

    # Set the background color to black
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    # Set the axis label and tick colors to white
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    x = []
    for item in sorted_avg_lengths.index:
        x.append(get_display(arabic_reshaper.reshape(item)))
        
    # Plot the sorted average story lengths as a bar plot with the specified bar color and white edges
    ax.bar(x, sorted_avg_lengths.values, color='#44c2b1', edgecolor='white', linewidth=1.5)

    # Add value labels to the top of each bar
    for i, value in enumerate(sorted_avg_lengths.values):
        x = i
        y = value
        formatted_length = f'{y:.2f}'  # Format the average length to two decimal places
        label = f'{formatted_length}'
        ax.text(x, y, label, ha='center', va='bottom', color='white', fontsize=10)

    # Rotate the x-axis labels by 90 degrees
    plt.xticks(rotation=90)

    if title:
        ax.set_title(title, color='white')
    # Show the plot
    plt.show()
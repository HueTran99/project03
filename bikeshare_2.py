import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york.csv',
              'washington': 'washington.csv' }

listMonth = {'January':1, 'Feburary':2, 'March':3, 'April':4, 'May':5, 'June':6}
listDayOfWeek = {"Monday": 0, "Tuesday":1,"Wednesday":2,"Thursday":3,"Friday":4, "Saturday":5,"Sunday":6 }

def check_input_month():
    """
     Input information about city, month and day for filter
    """
    while True:
            month = input("Which month? January, Feburary, March, April, May, or June?\n")
            month = month.capitalize()
            if listMonth.get(month) is not None:
                break

    print("You input month: " + month)
    return month

def check_input_day():
    """
       Input day of week: Sunday, Monday,...
    """
    while True:
             day = input("Which day?(Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday).\n")
             day = day.capitalize()
             
             if listDayOfWeek.get(day) is not None:
                break
                
    print("You input day: " + day)
    return day

def filter_condition():
    """
    The user enters informatio about city, month, and day to analyze.

    Returns:
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (str) city - name of the city to analyze  
    """
    city = 'chicago'
    month = "none"
    day = "none"
    
    print("Hello! Let's explore some US bikeshare data!")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Would you like to see data for Chicago, New York, or Washington?\n")
        city = city.lower()
        if city == "chicago" or city == "new york" or city == "washington":
            break

   

    # get user input for month (all, january, february, ... , june)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        validOptions = ['day','month','both','none']
        option = input("Would you like to filter the data by month, day, both, or not at all? Type 'none' for no time filter \n")
        option = option.lower()
        if option in validOptions:
            break

    if option == "both":
        month = check_input_month()
        day = check_input_day()
    elif option == "month":
        month = check_input_month()
    elif option == "day":
        day = check_input_day()

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print("Load data frame for: Citiy={}, month={}, day={}".format(city,month,day))
    filename = './' + CITY_DATA[city]
    print("Filename = ", filename)
    data = pd.read_csv(filename)
    print(data)
    """Convert Start Time to Datetime """
    data["Start Time"] = pd.to_datetime(data["Start Time"])

    """Fitler data by month and day."""
    if month != "none":
        print("Filter data by month\n")
        data = data[data["Start Time"].dt.month ==  listMonth.get(month)]

    if day != "none":
        print("Filter data by Day of week\n")
        data = data[data["Start Time"].dt.dayofweek == listDayOfWeek.get(day)]

    df = pd.DataFrame(data)
    print(df)

    return df

def time_travel(df):
    """Show statistics on the most frequent times of travel."""

    print('\The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Show the most common month
    month_travel = df["Start Time"].dt.month.value_counts()
    common_month = month_travel.idxmax()
    print("The most common month:", common_month)
    
    # Show the most common day of week
    day_travel = df["Start Time"].dt.dayofweek.value_counts()
    common_day = day_travel.idxmax()

    for key, value in listDayOfWeek.items():
        if value == common_day:
            print("The most common day of week:", key)
            break

    # Show the most common start hour
    hour_travel = df["Start Time"].dt.hour.value_counts()
    common_hour = hour_travel.idxmax()
    print("The most common hour: ", common_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_travel(df):
    """Show statistics on the most popular stations and trip."""

    print('\nThe Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Show the most commonly used start station
    start_statation = df["Start Station"].value_counts()
    common_start_station = start_statation.idxmax()
    print("The most commonly used start station: ", common_start_station)

    # Show the most commonly used end station
    end_statation = df["End Station"].value_counts()
    common_end_station = end_statation.idxmax()
    print("The most commonly used end station: ", common_end_station)

    # Show the most frequent combination of start station and end station trip
    group_combination = df.groupby(['Start Station', 'End Station']).size().reset_index(name='count')
    most_frequent = group_combination.loc[group_combination['count'].idxmax()]
    print("The most frequent combination:")
    frequent_station = "From " + \
    df['Start Station'] + " to " + df['End Station']
    station = frequent_station.mode()[0]
    print("Most Common Trip from Start to End: \n", station)
    print("Count: ", most_frequent['count'])
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)                      

def trip_duration(df):
    """Show statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # show the total travel time.
    total_duration = df['Trip Duration'].sum()
    total_minute, total_second = divmod(total_duration, 60)
    total_hour, total_minute = divmod(total_minute, 60)
    print("Total Travel Time: \n", str(round(total_hour)) + ':' +
      str(round(total_minute)) + ':' + str(round(total_second)))

    # show the average travel time.
    average_duration = round(df['Trip Duration'].mean())
    average_minute, average_second = divmod(average_duration, 60)
    average_hour, average_minute = divmod(average_minute, 60)
    print("Average Travel Time: \n", str(round(average_hour)) + ':' +
      str(round(average_minute)) + ':' + str(round(average_second)))

    print("\nThat took %s seconds." % (time.time() - start_time))
    print('*'*50)

def user_stats_infomation(df, city):
    """Show statistics on bikeshare users."""

    print('\nShow user information...\n')
    start_time = time.time()

    # show the information user type
    user_type = df['User Type'].value_counts()
    print("Counts of Each User Type: ")
    print('Subscriber: ', user_type['Subscriber'])
    print('Customer: ', user_type['Customer'])

    # show the information of gender and birth year if the city is Chicago or New York
    if city in ['chicago', 'new york']:
        gender = df['Gender'].value_counts()
        print('\nCounts of Each Gender: ')
        print('Male: ', gender['Male'])
        print('Female: ', gender['Female'])

        print('\nEarliest Year of Birth: ', int(df['Birth Year'].min()))
        print('Most Recent Year of Birth: ', int(df['Birth Year'].max()))
        print('Most Common Year of Birth: ', int(df['Birth Year'].mode()[0]))

    print("\nThat took %s seconds." % (time.time() - start_time))
    print('*'*50)


def display_data(df):
    """ Display raw data """
    i = 0
    raw = input("Do you want to view raw data? (yes/no)\n").lower()
    # TO DO: convert the user input to lower case using lower() function
    pd.set_option('display.max_columns',200)
    
    while True:            
        if raw == 'no':
            break
        elif raw == 'yes':
            print(df.iloc[i:(i+5)])
            raw = input("Would you like to view raw data? (yes/no)\n").lower()
            i += 5
        else:
            raw = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()

def main():
    while True:
        try:
            city, month, day = filter_condition()
            df = load_data(city, month, day)
        
            time_travel(df)
            station_travel(df)
            trip_duration(df)
            user_stats_infomation(df, city)
            display_data(df)

            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break
        except BaseException:
            print("The data is invalid!")

if __name__ == "__main__":
	main()

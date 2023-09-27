import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). 
    while True:
        city = input("\nWould you like to see data from chicago, new york city or washington ?\n")
        if city not in ('chicago', 'new york city', 'washington'):
            print("Please, make a choice among the stated cities")
            continue
        else:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input(
            "\nWich month do you want to filter by ? Type january', 'february', 'march', 'april', 'may', 'june' or type 'all' to ignore the filtering\n")
        if month not in ("all", "january", "february", "march", "april", "may", "june"):
            print("\nPlease select a number from the given list !")
            continue
        else:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input(
            "\nDo you want to filter by a specific day ? Type monday,tuesday, wednesday, thursday, friday, saturday or sunday to select a day or type 'all' to ignore the filtering\n")
        if day not in ("all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"):
            print("\nPlease select a number from the given list !")
        else:
            break

    print('-' * 40)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

        # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print("\nMost common month:", popular_month)

    # TO DO: display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print("\nMost common day of week:", popular_day_of_week)

    # TO DO: display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print("\nThe Most common start hour:", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].value_counts().idxmax()
    print("\nMost commonly used start station:", most_common_start_station)

    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].value_counts().idxmax()
    print("\nMost commonly used end station:", most_common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    most_frequent_combination_gb = df.groupby(['Start Station', 'End Station'])
    most_frequent_combination = most_frequent_combination_gb['Trip Duration'].count().idxmax()

    print("\nMost frequent combination of start station and end station trip:", most_frequent_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("\nTotal travel time:", total_travel_time / 3600, "Hours")

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("\nMean travel time:", mean_travel_time / 60, "Minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print("\nCounts of user types:", user_types)

    # TO DO: Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print("\nCounts of gender:", gender)
    except KeyError:
        print("\nCounts of gender: there is no data for this month")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest_birthdate = df['Birth Year'].min()
        print("\nEarliest year of birth:", earliest_birthdate)
    except KeyError:
        print("\nEarliest year of birth: there is no data for this month")

    try:
        most_recent_birthdate = df['Birth Year'].max()
        print("\nMost Recent Year:", most_recent_birthdate)
    except KeyError:
        print("\nMost recent year of birth: there is no data for this month")

    try:
        most_common_birthdate = df['Birth Year'].value_counts().idxmax()
        print("Most common year of birth:", most_common_birthdate)
    except KeyError:
        print("\nMost common year of birth: there is no data for this month")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_data(df,a,b):
    """Display 5 lines of raw data each time the user says "yes" and stop displaying when he says "no" """

    while True:
        #Get user input on wether he wants to display raw data
        user_choice = input("\nWould you like to see raw data ? Type 'yes' to display 5 lines of raw data or 'no' to stop the display.\n")
        user_choice = user_choice.lower()
        if user_choice not in ("yes","no"):
            print("\nPlease, you must choose between 'yes' or 'no'")
            continue
    #  Display 5 lines of raw data
        if user_choice == "yes":
            raw_data = df.iloc[a:b]
            print(raw_data)
            a = b
            b = b+5
            continue
        if user_choice == "no":
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
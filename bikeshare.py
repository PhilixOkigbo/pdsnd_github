import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    user_name = input('Please enter your name...')
    print('Hello {}! Let\'s explore some US bikeshare data!'.format(user_name))
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("What city are you interested in: Chicago, New York City or Washington?\n" + ('-----' * 5)+'\n').lower()
        if city not in ('new york city', 'chicago', 'washington'):
            print("You have entered an invalid city please a valid one!")
            continue
        else:
            break


    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Which month would you like to explore? (Please select from January, February, March, " + "April, May and June, or type all to explore all months.\n" + ('-----' * 5)+'\n').lower()
        if month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            print("You have entered an invalid month please a valid one!")
            continue
        else:
            break


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Please select the day you  would like to explore: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday, or type all  for all days \n"+ ('-----' * 5)+'\n').lower()
        if day not in ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all'):
            print("You have entered an invalid day please a valid one!")
            continue
        else:
            break


    print('-'*50)
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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    df['weekday'] = df['Start Time'].dt.weekday
    df['Start hour'] = df['Start Time'].dt.hour
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    
    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day)
        df = df[df['weekday'] == day]

    
    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month != 'all':
        print('The most popular month : ' + month)
    else:
        popular_month = df['month'].mode()[0]
        print('The most common month: ', popular_month)

    # display the most common day of week
    if day != 'all':
        print('The most popular day : ' + day)
    else:
        popular_day = df['weekday'].mode()[0]
        print('The  most common day of thw week: ', popular_day)

    # display the most common start hour
    print('The most common start hour :', 
          df['Start hour'].mode().to_string(index=False, header=False))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('\ncommonly used start station : ' + common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('\ncommonly used end station : ' + common_end_station)

    # display most frequent combination of start station and end station trip
    station_combination = df['Start Station'] + " - " +  df['End Station']
    common_station_combination = station_combination.mode()[0]
    print('\nfrequently used station combination : ' + common_station_combination)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    trip_hours = total_duration / 60 / 60
    print('\nTotal travel time : ' + str(round(trip_hours, 2)) + ' hours')
    
    # display mean travel time
    avg_total_duration = df['Trip Duration'].mean()
    avg_trip_hours = avg_total_duration / 60 / 60
    print('\nAverage travel time : ' + str(round(avg_trip_hours, 2)) + ' hours')
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of user types: \n", user_types.to_frame())

    # Display counts of gender
    if city != 'washigton':
        gender = df.Gender.value_counts()
        print('\nCount of gender : \n', gender.to_frame())
    else: 
        print('\nNo gender data available for the selected city')
    
    
    # Display earliest, most recent, and most common year of birth
    if city != 'washigton':
        birth_year = df['Birth Year'].dropna()
        print('\n Earliest birth year: ', birth_year.min(),\
             '\n Most recent birth year: ', birth_year.max(),\
             '\n Most common birth year: ', birth_year.mode().to_string(index=False, header=False))
    else: 
        print('\nNo Birth year data available for the selected city')
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)



def raw_data(df):
    """ This would display 5 lines of raw data when user enters 'yes' as input"""
    start = 1
    while True:
        response = input('\nDo you want to see 5 lines on the raw data used in the computation? Enter yes or no \n')
        if response.lower() == 'yes':
            print(df[start:start + 5])
            start += 5
        else: 
            break

    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()


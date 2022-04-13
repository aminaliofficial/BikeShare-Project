import time
import pandas as pd

# Read CSV files!
CITY_DATA = { 
                'chicago'   : 'Data/chicago.csv',
                'new york'  : 'Data/new_york_city.csv',
                'washington': 'Data/washington.csv' 
            }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Args:
        None.
    Returns:
        str (city): name of the city to analyze
        str (month): name of the month to filter by, or "all" to apply no month filter
        str (day): name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Select city from user!
    city = input('Would you like to see data for Chicago, New York, or Washington?: ')
    while city not in(CITY_DATA.keys()):
        print('Invalid Input! Please try again')
        city = input('Would you like to see data for Chicago, New York, or Washington?: ').lower()

    # Choosing type of Filter such as: month, day, both, none!
    filter = input('Would you like to filter the data by month, day, both, or none?: ').lower()
    while filter not in(['month', 'day', 'both', 'none']):
        print('Invalid Input! Please try again')
        filter = input('Would you like to filter the data by month, day, both, or none?: ').lower()

    # Filtering by month!
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    if filter == 'month' or filter == 'both':
        month = input('Which month? : January, February, March, April, May, or June?: ').lower()
        while month not in months:
            print('Invalid Input! Please try again')
            month = input('Which month? : January, February, March, April, May, or June?: ').lower()
    else:
        month = 'all'

    # Filtering by day!
    days = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    if filter == 'day' or filter == 'both':
        day = input('Which day? : Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday or Friday : ').title()
        while day not in days:
            print('Invalid Input! Please try again')
            day = input('Which day? : Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday or Friday : ').title()
    else:
        day = 'all'

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    # Load CSV file into a DataFrame(df)
    df = pd.read_csv(CITY_DATA[city])

    # convert 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract 'month' and 'day of week' from 'Start Time' column to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

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
    print('\nCalculating The Most Frequent Times of Travel. \n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = df['month'].mode()[0]
    print(f'The most common month is        : {months[month-1]}')

    # display the most common day of week
    day = df['day_of_week'].mode()[0]
    print(f'The most common day of week is  : {day}')

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print(f'The most common start hour is   : {popular_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip. \n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print(f'The most popular start station is  : {popular_start_station}')

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print(f'The most popular end station is    : {popular_end_station}')

    # display most frequent combination of start station and end station trip
    popular_trip = df['Start Station'] + ' to ' + df['End Station']
    print(f'The most popular trip is           : from {popular_trip.mode()[0]}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    print('\nCalculating Trip Duration. \n')
    start_time = time.time()

    # display total travel time
    total_travel_duration = (pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])).sum()
    days =  total_travel_duration.days
    hours = total_travel_duration.seconds // (60*60)
    minutes = total_travel_duration.seconds % (60*60) // 60
    seconds = total_travel_duration.seconds % (60*60) % 60
    print(f'Total travel time is   : {days} days {hours} hours {minutes} minutes {seconds} seconds')

    # display mean travel time
    average_travel_duration = (pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])).mean()
    days =  average_travel_duration.days
    hours = average_travel_duration.seconds // (60*60)
    minutes = average_travel_duration.seconds % (60*60) // 60
    seconds = average_travel_duration.seconds % (60*60) % 60
    print(f'Average travel time is : {days} days {hours} hours {minutes} minutes {seconds} seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    print('\nCalculating User Stats. \n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print(user_type)
    print('\n\n')

    # Display counts of gender
    if 'Gender' in(df.columns):
        gender = df['Gender'].value_counts()
        print(gender)
        print('\n\n')

    else:
        print("\nThere is no 'Gender' column in this file.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in(df.columns):
        year = df['Birth Year'].fillna(0).astype('int64')
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f'Earliest birth year is    : {earliest}\nMost recent is            : {recent}\nMost common birth year is : {common_year}')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('\n'+'-'*40)

def display_raw_data(df):
    raw = input('\nWould you like to view more raw data?(yes or no): ')
    print()
    if raw.lower() == 'yes':
        count = 0
        while True:
            print(df.iloc[count: count+5])
            count += 5
            ask = input('Next 5 raws?(yes or no): ')
            if ask.lower() != 'yes':
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart?(yes or no): ')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

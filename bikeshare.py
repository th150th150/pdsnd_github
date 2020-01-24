import time
import sys
import pandas as pd
import numpy as np

# define global variables

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = list(CITY_DATA)
months = ['january', 'february', 'march', 'april', 'may', 'june']
days =['sunday','monday','tuesday','wednesday','thursday','friday','saturday']

# we define get_filters to prompt user for city, month and day to analyze

def get_filters():

    #define variables used within function

    city = " "
    month = " "
    day = " "

    attempts = 0
    while city not in cities:
        city = input("Enter city - name of the city to analyze: ").lower()
        if city in cities:
            print(city.title(),'- got it!')
        elif attempts == 3:
            print('Please ask for help!')
            sys.exit()
        elif city not in cities:
            attempts += 1

    attempts = 0
    while month not in months and month != 'all':
        month = input("month - name of the month to filter by, or \"all\" to apply no month filter: ").lower()
        if month in months or month == 'all':
            print(month.title(),'= got it!')
        elif attempts == 3:
            print('Please ask for help!')
            sys.exit()
        attempts += 1

    attempts = 0
    while day not in days and day != 'all':
        day = input("Enter day - name of the day of week to filter by, or \"all\" to apply no day filter: ").lower()
        if day in days or day == 'all':
            print(day.title(),'- got it!')
        elif attempts == 3:
            print('Please ask for help!')
            sys.exit()
        attempts += 1

    return city, month, day

# we def load_data to read csv file relevate to city selected by user

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
    # load data file into a dataframe - code derived from Practice Problem #3
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

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

# The following four function display statistics from selected city's csv file

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    # inspried by Udacity practiceSolution1
    popular_month = df['month'].mode()[0]
    print("Most common month: ", popular_month)

    # TO DO: display the most common day of week
    # inspried by Udacity practiceSolution1
    popular_dow = df['day_of_week'].mode()[0]
    print("Most common day of week: ", popular_dow)

    # TO DO: display the most common start hour
    # given by Udacity practiceSolution1
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("Most common start hour: ", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # inspired by Udacity's practiceSolution1

    # TO DO: display most commonly used start station
    popular_startStation = df['Start Station'].mode()[0]
    print("Most commonly used Start Station: ", popular_startStation)

    # TO DO: display most commonly used end station
    popular_endStation = df['End Station'].mode()[0]
    print("Most commonly used End Station: ", popular_endStation)

    # TO DO: display most frequent combination of start station and end station trip
    df['seComboLocation'] = "Start: " + df['Start Station'] + " End: " + df['End Station']
    popular_comStation = df['seComboLocation'].mode()[0]
    print("Most most frequent combination of start station and end station: ", popular_comStation)

    print("\nThis took %s seconds." % round(float(time.time() - start_time),4))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    # methods inspired by https://pandas.pydata.org/pandas-docs/stable/reference/index.html
    # time converstion inspired by https://www.w3resource.com/python-exercises/python-basic-exercise-62.php
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    sumTravelTime = int(df['Trip Duration'].sum())
    sumDays = round(sumTravelTime / 3600 / 24)
    sumHours = round(sumTravelTime / 3600)
    sumMinutes = round(sumTravelTime / 60)
    sumSeconds = sumTravelTime % 60
    print('Sum Trip Duration: {} days, {} hours, {} minutes, {} seconds'.format(sumDays, sumHours, sumMinutes, sumSeconds))

    # TO DO: display mean travel time
    meanTravelTime = int(df['Trip Duration'].mean())
    meanMinutes = round(meanTravelTime / 60)
    meanSeconds = meanTravelTime % 60
    print('Mean Trip Duration: {} minutes, {} seconds'.format(meanMinutes, meanSeconds))

    print("\nThis took %s seconds." % round(float(time.time() - start_time),4))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    #citation: given by practiceSolution2
    user_types = df['User Type'].value_counts()
    print('\nTypes of users:\n',user_types)


    # TO DO: Display counts of gender
    # not all city file(s) contain gender, so we skip if unavilable
    if 'Gender' not in df:
        print('\nUser gender not available for this city!')
    elif 'Gender' in df:
        user_gender = df['Gender'].value_counts()
        print('\nUsers by gender\n',user_gender)

    # TO DO: Display earliest, most recent, and most common year of birth
    # not all city file(s) contain user birth info, so we skip if unavilable
    # citation http://www.datasciencemadesimple.com/mode-function-python-pandas-dataframe-row-column-wise-mode/
    if 'Birth Year' not in df:
        print('\nUser birth information not available for this city!')
    elif 'Birth Year' in df:
        print('\nEarliest year of birth was ',int(df.loc[:,'Birth Year'].min()))
        print('\nMost recent year of birth was ',int(df.loc[:,'Birth Year'].max()))
        print('\nMost common year of birth year was ',int(df.loc[:,"Birth Year"].mode()))

    print("\nThis took %s seconds." % round(float(time.time() - start_time),4))
    print('-'*40)

# we create seeData to prompt user to see a sample of data after viewing stats

def seeData(df):

    # we define showMore() to display sample of five rows of data

    def showMore(df):
        moreDataInd = 1
        rangeStart = 0
        rangeEnd = 5

        while moreDataInd ==1:
            for i in range(rangeStart, rangeEnd):
                print(df.iloc[i])

            rangeStart += 5
            rangeEnd += 5
            wantEvenMore = input('Display 5 more lines? Enter yes or no.\n ').lower()

            if wantEvenMore =='yes':
                continue
            elif wantEvenMore !='yes':
                moreDataInd = 0
                break
            else:
                print('Moving on!\n')
            return
        return

    # once sample is displayed, we prompt if user wants another sample
    # if response is affirmative, we then call showMore()
    wantMore = input('Display 5 lines of raw data? Enter yes or no.\n ').lower()
    if wantMore == 'yes':
        showMore(df)
    else:
        print('Moving on!\n')
        return

# we defin main() to call functions of our script in desired sequence

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        seeData(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()

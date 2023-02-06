#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time
import pandas as pd

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

    days = ["Sunday", "Monday", "Tuesday", "Wednesday","Thursday", "Friday", "Saturday" ] 
    months= [ 'january', 'february', 'march', 'april', 'may', 'june']

    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        try:
            city = input('Would you like to see data for Chicago, New York City or Washington? \n>').lower()
            if city in CITY_DATA.keys():
                break
        except:
            print('Error. Please enter city chicago, new york city or washington.\n')
        
    while True:
        try:
            filters =input('Would you like to filter by month, day, both, or none? \n>').lower()
            if filters in ['day','month','both','none']:
                break
        except:
            print('Error. please enter right value.')  

    if filters=='month':
        while True:
            try:
                month=input('Which month? {} \n>'.format(months)).lower()
                if month in months:
                    break
            except:
                print("Error. enter correct month")

        day='all'

    elif filters=='day':
        while True:
            try:
                day=input('Which day? {} \n>'.format(days)).title()
                if day in days:
                    break
            except:
                print("Error. try enter correct day")
        month='all'
    
    elif filters=='both':
        while True:
            try:
                month=input('Which month? {} \n>'.format(months)).lower()
                day=input('Which day? {} \n>'.format(days)).title()
                if month in months and day in days:
                    break           
            except:
                print("Error.try again") 
    
    else:
        month,day='all','all'
   
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

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month']=df['Start Time'].dt.month
    df['day_of_week']=df['Start Time'].dt.day_name()
    df['hour']=df['Start Time'].dt.hour


    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day]    
    
    
    return df
    
    

def time_stats(df,day,month):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # the most common month

    if month=='all':
        most_common_month = df['month'].mode()[0]
        print('The most common month is :', most_common_month)

    # the most common day of week
    if day=='all':
        most_common_day_of_week = df['day_of_week'].mode()[0]
        print('The most common day of week is :', most_common_day_of_week)


    # the most common start hour




    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # most commonly used start station

    most_common_start_station = df['Start Station'].mode()[0]
    print(" The most commonly used start station :", most_common_start_station)
   
    # display most commonly used end station

    most_common_end_station = df['End Station'].mode()[0]
    print("The most common used end station :", most_common_end_station)

    #most frequent combination of start station and end station trip

    df['most_common_start_to_end_stations'] = df['Start Station']+" to "+df['End Station']
    print('The most frequent combination for start to end station : {}'.format(df['most_common_start_to_end_stations'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    total_travel = df['Trip Duration'].sum()
    print("Total travel time:", total_travel)

    # display mean travel time
    
    mean_travel = df['Trip Duration'].mean()
    print(" Mean travel time :", mean_travel)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    user_counts = df['User Type'].value_counts()
    print(" Counts of user types:\n",user_counts)


    # iteratively print out the total numbers of user types
    customers=0
    subscribers=0
    dependants=0
    for i in range(len(df["User Type"])):
        if df['User Type'].iloc[i]=="Customer":
            customers+=1
        elif df['User Type'].iloc[i]=="Subscriber":
            subscribers+=1
        else:
            dependants+=1
    print(f"\n\nIteratively, number of custumers:{customers}\n    Number of subscribers: {subscribers}\n    Number of dependant: {dependants}")

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of gender:\n",gender_counts)
  


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest=df['Birth Year'].min()
        print('earliest birth year:',earliest)
        most_recent=df['Birth Year'].max()
        print("most recent birth year:",most_recent) 
        most_common_year = df['Birth Year'].mode()[0]
        print('The most common birth year:', most_common_year)
   


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        # Getting required parameters for stats functions
        city, month, day = get_filters()
        df = load_data(city, month, day)
        # Stats functions
        time_stats(df,day,month)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        # Asking the user if they want to restart the program
        restart = input('\nWould you like to restart? Enter yes or no \n')
        if restart.lower() != 'yes':
            break

    # Asking the user if they want to view raw inputs   
    count=5
    checker='yes'
    while checker=='yes':
        checker=input('do you want to explore raw input? \nenter yes for more or anything else to exit \n').lower()
        if checker!='yes':
            break
        else:
            print(df.head())
        while True:
            checker=input("Do you want to display more raw input? enter yes for more or anything else to exit \n").lower()
            if checker!='yes':
                break
            else:
                print(df.iloc[count:].head())
                count+=5
                  
    print('Thank you, see you later')

if __name__ == "__main__":
	main()


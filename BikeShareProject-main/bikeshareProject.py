import pandas as pd
import numpy as np

def display_raw_data(df):
    """
    displays raw data to the user
    :param df: data frame ,the which will be displayed
    :return: no return value
    """
    counter = 5
    pd.set_option('display.max_columns', 200)
    print(df.head(counter))
    while True:
        while True:
            display_more = input("would you like to display more data?(yes/no)")
            # safeguard to prevent the user from wrong answer in the input
            if (not display_more.isalpha()) and (display_more.lower() in ['yes', 'no']):
                print("Please Type your Answer Correctly!")
                continue
            else:
                break

        if (display_more.lower() == 'yes') and (counter != (len(df) - 1)):
            counter += 5
            pd.set_option('display.max_columns', 200)
            print(df.head(counter))

        # safeguard to prevent the user from entering invalid input
        elif display_more.lower() == 'no':
            break
        else:
            print("Please Enter Correct Answer (yes/no)!")
            continue


def calculate_percentage(filtered_data, max_boundary, min_boundary):
    """
    computes the percentage of some specified age category of bike users
    :param filtered_data: data frame, which will be used in filtering the specified category
    :param max_boundary: int,max age of the category
    :param min_boundary: int,min age of the category
    :return: float, percentage of this category to bike users
    """
    total_num_user = len(filtered_data)
    total_num_user_category = len(filtered_data[(filtered_data['Age'] > min_boundary) &
                                                (filtered_data['Age'] < max_boundary)])
    return round((total_num_user_category / total_num_user) * 100, 2)


def pre_processing():
    """
    this function removes the missing values and extract new features from data
    :return: a dict contains 3 preprocessed data frames
     with the name of the city as a key and the value is the data frame
    """
    # load the data
    chicago_df = pd.read_csv('datasets/chicago.csv')
    new_york_df = pd.read_csv('datasets/new_york_city.csv')
    washington_df = pd.read_csv('datasets/washington.csv')
    data_list = [chicago_df, new_york_df, washington_df]
    day_map = {0: 'monday', 1: 'tueday', 2: 'wedday', 3: 'thuday', 4: 'friday', 5: 'satday', 6: 'sunday'}

    # remove NA values
    for df in data_list:
        df.dropna(inplace=True)

    # converting to a datetime object
    for df in data_list:
        df['End Time'] = pd.to_datetime(df['End Time'])
        df['Start Time'] = pd.to_datetime(df['Start Time'])

    # creating new date features
    for df in data_list:
        df['Month'] = df['Start Time'].apply(lambda time: time.month)
        df['Start hour'] = df['Start Time'].apply(lambda time: time.hour)
        df['End hour'] = df['End Time'].apply(lambda time: time.hour)
        df['Day of Week'] = df['Start Time'].apply(lambda time: time.dayofweek)
        # mapping day numbers to day names
        df['Day of Week'] = df['Day of Week'].map(day_map)

    # creating age feature only for NYC and Chicago
    for df in data_list[0:2]:
        df['Age'] = df['Birth Year'].apply(lambda year: 2022 - year)
    # dropping unused features
    for df in data_list:
        df.drop(['Unnamed: 0', 'Start Time', 'End Time'], axis=1, inplace=True)

    city_dict = {'chicago': data_list[0],
                 'newyork': data_list[1],
                 'washington': data_list[2]}
    return city_dict


def apply_filter(city, time_filter='none', month=['none'], day=['none']):
    """
    Apply the specified time filters to the data frame
    :param city: data frame of the chosen city
    :param time_filter: str, if equal to 'none' no time filter is specified, default 'None'
    :param month: list of str, if equal to 'none' no month is specified, default 'None'
    :param day: list of str, if equal to 'none' no day is specified, default 'None'
    :return: no return value
    """

    if time_filter.lower() != 'none':
        if (month != ['none']) and (day != ['none']):
            stats(city[(city['Month'].isin(month)) & (city['Day of Week'].isin(day))])
        elif month != ['none']:
            stats(city[city['Month'].isin(month)])
        else:
            stats(city[city['Day of Week'].isin(day)])
    else:
        stats(city)


def stats(filtered_data):
    """
    Compute and Display statistics of the filtered data
    :param filtered_data: filtered data frame
    :return: no return value
    """
    # Popular times of travel stats
    print('\nCalculating Popular Times Stats...\n')
    print('-' * 20)
    print('Most Common Month:', filtered_data['Month'].mode()[0])
    print('Most Common Day:', filtered_data['Day of Week'].mode()[0] + 'Day')
    print('Most Common Start Trip Hour:', filtered_data['Start hour'].mode()[0])
    print('Most Common End Trip Hour:', filtered_data['End hour'].mode()[0])
    print('-' * 20)
    # Popular stations and trip stats
    print('\nCalculating Popular stations and trip Stats...\n')
    print('-' * 20)
    print('Most Common Start Station:', filtered_data['Start Station'].mode()[0])
    print('Most Common End Station:', filtered_data['End Station'].mode()[0])
    print('Most Common Start-End Station:',
          filtered_data[['Start Station', 'End Station']].apply(lambda x: (x[0], x[1]), axis=1).mode()[0])
    print('-' * 20)
    # 3 Trip duration stats
    print('\nCalculating Trip Duration Stats...\n')
    print('-' * 20)
    print('Total Trips Duration in hrs:', (filtered_data['Trip Duration'].sum()) / 3600)
    print('Average Trips Duration in mins:', (filtered_data['Trip Duration'].mean()) / 60)
    print('Max Trip Duration in hrs:', round(filtered_data['Trip Duration'].max() / 3600, 2))
    print('Min Trip Duration in sec:', round(filtered_data['Trip Duration'].min(), 2))
    print('-' * 20)
    # 4 Users info stats
    print('\nCalculating Users Info Stats...\n')
    print('-' * 20)
    print('BikeShare User Types And its Count:\n', filtered_data['User Type'].value_counts().to_string())
    if 'Gender' and 'Birth Year' in filtered_data:  # guard to washington df which does not include these columns
        print('BikeShare User Gender And its Count:\n', filtered_data['Gender'].value_counts().to_string())
        print('Oldest BikeShare User Birth Year:', filtered_data['Birth Year'].min())
        print('Youngest BikeShare User Birth Year:', filtered_data['Birth Year'].max())
        print('Most Common BikeShare Users Birth Year:', filtered_data['Birth Year'].mode()[0])
        print('Oldest BikeShare User Age:', filtered_data['Age'].max())
        print('Youngest BikeShare User Age:', filtered_data['Age'].min())
        print('{} % of bike riders is teens(15-20 Yrs):'.format(calculate_percentage(filtered_data, 20, 15)))
        print('{} % of bike riders is young(20-40 Yrs):'.format(calculate_percentage(filtered_data, 40, 20)))
        print('{} % of bike riders is old(40-60 Yrs):'.format(calculate_percentage(filtered_data, 60, 40)))
        print('{} % of bike riders is very old(60-90 Yrs):'.format(calculate_percentage(filtered_data, 90, 60)))
    print('-' * 20)


def main():
    data_frames = pre_processing()
    day_set = {'monday', 'tueday', 'wedday', 'thuday', 'friday', 'satday', 'sunday'}
    month_set = {'1', '2', '3', '4', '5', '6'}
    while True:
        print('Hi And Welcome To BikeShare Project!\n')
        while True:
            city = input("Please Choose Which City you Would Like to Explore! "
                         "(Chicago, NewYork, Washington)\n>")
            time_filter = input("Alright...\nWould you Like to filter The Data by 'Month', 'Day','both'(month,day) or "
                                "no filter(Please type 'None' in case you do not want any time filter)\n>")
            # safeguard to prevent the user from entering numbers or spaces  in the input
            if not city.isalpha():
                print("Please Do Not Enter Numbers or Spaces in the City Name And Retry Again !")
                continue
            elif not time_filter.isalpha():
                print("Please Do Not Enter Numbers or Spaces in Time Filter And Retry Again !")
                continue
            # safeguard to prevent the user from entering the input incorrectly
            elif not (city.lower() in ['chicago', 'newyork', 'washington']):
                print("Please Enter The Name of The City Correctly And Retry Again !")
                continue
            elif not (time_filter.lower() in ['month', 'day', 'both', 'none']):
                print("Please Enter The Time Filter Correctly And Retry Again !")
                continue
            else:
                break

        if time_filter.lower() != 'none':
            while True:
                if time_filter.lower() == 'month':
                    month = input("Please Enter The month(s).\nNote : Available months are (1,2,3,4,5,6)\n"
                                  "Enter The Values Separated by one space\n>").split()
                    day = ['none']
                elif time_filter.lower() == 'day':
                    day = input("Please Enter The day(s).\nNotes :\n1-Mon Day is the start of the week\n2-Type "
                                "The abbreviation of the day i.e. Wednesday -> wed) \n"
                                "3-Enter The Values Separated by one space\n>").split()
                    month = ['none']
                else:
                    month = input("Please Enter The month(s).\nNote : Available months are (1,2,3,4,5,6)\n"
                                  "Enter The Values Separated by one space\n>").split()
                    day = input("Please Enter The day(s).\nNotes :\n1-Mon Day is the start of the week\n2-Type "
                                "The abbreviation of the day i.e. Wednesday -> wed) \n"
                                "3-Enter The Values Separated by one space\n>").split()
                # safeguard to prevent the user from entering Characters in the input
                if (not all([x.isdigit() for x in month])) and (month != ['none']):
                    print("Please Do Not Enter Characters When Selecting Month(s) in Your Answer And Retry Again !")
                    continue
                # safeguard to prevent the user from entering numbers in the input
                elif (all([x.isdigit() for x in day])) and (day != ['none']):
                    print("Please Do not Enter Numbers When Selecting Day(s) in Your Answer And Retry Again !")
                    continue
                # safeguard to prevent the user from entering invalid format in the input
                elif (not all([x in month_set for x in month])) and (month != ['none']):
                    print("Please Enter The Month(s) Name as the specified format and Retry Again !")
                    continue
                # safeguard to prevent the user from entering invalid format in the input
                elif (not all([x.lower() in day_set for x in day])) and (day != ['none']):
                    print("Please Enter The Day(s) Name as the specified format and Retry Again !")
                    continue
                else:
                    break
        else:
            month = ['none']
            day = ['none']

        day = list(map(lambda x: x.lower(), day))  # format the day input to match the format in the data frames
        print('\nThe Displayed Stats Are Filtered by:')
        print('Month:', month)
        print('day:', day)
        print('-'*20)
        print('\n')
        apply_filter(data_frames[city.lower()], time_filter, month, day)

        while True:
            display_raw = input("Would you like to Display The raw Data? (yes/no)")
            # safeguard to prevent the user from wrong answer in the input
            if (not display_raw.isalpha()) and (display_raw.lower() in ['yes', 'no']):
                print("Please Type your Answer Correctly!")
                continue
            elif display_raw.lower() == 'yes':
                display_raw_data(data_frames[city.lower()])
                break
            elif display_raw.lower() == 'no':
                break
            else:
                print("Please Enter Correct Answer (yes/no)!")
                continue

        while True:
            explore_again = input("Would you like to explore another city? (yes/no)")
            # safeguard to prevent the user from wrong answer in the input
            if (not explore_again.lower() in ['yes', 'no']) or (not explore_again.isalpha()):
                print("Please Type your Answer Correctly!")
                continue
            else:
                break
        if explore_again.lower() == 'yes':
            continue
        else:
            break



if __name__ == "__main__":
    main()

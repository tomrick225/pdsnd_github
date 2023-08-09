import time
import pandas as pd


# Sleep seconds to present the output by pieces
sleep_sec = 2.0         

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Basic dictionaries
months = {1:"January",
          2:"February",
          3:"March",
          4:"April",
          5:"May",
          6:"June",
          7:"all"}

weekdays = {1:"Monday",
            2:"Tuesday",
            3:"Wednesday",
            4:"Thursday",
            5:"Friday",
            6:"Saturday",
            7:"Sunday",
            8:"all"}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a 
    # while loop to handle invalid inputs
    city = 0
    while city == 0:
        given_city = input("1   Would you like to see data for Chicago, "
                           "New York City or Washington? \n").lower()
        if given_city in CITY_DATA:
            city = given_city.lower()
        else:
            print("Seems like no valid input. Please try again. Mind the spelling.")
    print("Your city of choice: ",city)

    # find out, if the user wants to apply filter(s)
    choice = 0
    options = {1:"yes",
               2:"no"}
    while choice == 0:
        try:
            given_choice = int(input("Would you like to filter the data? \n"
                                     " yes --> press 1 \n" 
                                     " no  --> press 2 \n"))
            if given_choice in [1,2]:
                choice = given_choice
        except ValueError:
            print("Seems like no valid input. Please try again." 
                  "You can choose between option 1 or 2.")
    print("Your choice on filtering: ", options[choice])

    # get user input for month (all, january, february, ... , june) and
    #     user input for weekday (all, monday, tuesday, ... sunday)
    if choice == 1:
        month = 0
        month_num = 0
        
        while month == 0:
            try:
                month_num = int(input("3 Which month would you like to see? Press \n"
                                      "'1' for January, \n"
                                      "'2' for February, \n"
                                      "'3' for March, \n"
                                      "'4' for April, \n"
                                      "'5' for May,\n"
                                      "'6' for June or \n" 
                                      "'7' for all months \n",))
                if month_num in months.keys():
                    month = months[month_num]
                else:
                    print("Seems like no valid input. Please try again."
                          "You can choose between option 1,2,3,4,5,6 and 7.")
            except ValueError: 
                    print("Seems like no valid input. Please try again.")
        print("Your choice: {} -> {}\n".format(month_num, month))
 
    # get user input for day of week (all, monday, tuesday, ... sunday) 
        day = 0
        day_num = 0
        
        while day == 0:
            try:
                day_num = int(input("4 Which day would you like to choose? Press \n"
                                    "'1' for Monday, \n"
                                    "'2' for Tuesday, \n"
                                    "'3' for Wednesday, \n"
                                    "'4' for Thursday, \n"
                                    "'5' for Friday, \n"
                                    "'6' for Saturday,\n"
                                    "'7' for Saturday or \n"
                                    "'8' for all weekdays?\n"))
                #print(day_num)
                if day_num in weekdays.keys():
                    day = weekdays[day_num]
            except ValueError:
                print("Seems like no valid input. Please try again."
                      "You can choose between option 1,2,3,4,5,6,7 and 8.")
        print("Your choice: {} -> {}".format(day_num, day))

    # set parameters when no filter is wished: 
    if choice == 2:
        month = 'all'
        day   = 'all'
    
    print("Your final choice: \n city :{}\n month:{}\n day  :{}".format(city,month,day))
    print('-'*40)
    return city, month, day
    # return-example: 'new york city', 'January' , 'monday'

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month, day of week and hour from Start Time to create new columns
    #df['month'] = df['Start Time'].dt.month  -> alt: als Zahl
    df['month'] = df['Start Time'].dt.strftime('%B')
    #df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    
    # convert Trip Duration for Washington data into sec
    if city == 'washington':
        df['Trip Duration'] = df['Trip Duration'].apply(lambda x: x/60)

    # filter by month if applicable
    if month != 'all':
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

    # Example:
    # df = load_data('new york city', 'January' , 'monday')

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    
    print("Most common month within your given search parameters: ", popular_month)

    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    
    print("Most common day of week within your given search parameters: ", popular_day_of_week)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    
    print("Most common start hour: ", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    time.sleep(sleep_sec)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("Most commonly used start station: ", popular_start_station)
    
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("Most commonly used end station:   ", popular_end_station)

    # display most frequent combination of start station and end station trip
    # combine the data from start station column and end station column to create a Route column
    df['Route'] = df['Start Station'] + "-" + df['End Station']
    popular_route = df['Route'].mode()[0]
    print("Most commonly used route:         ", popular_route)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    time.sleep(sleep_sec)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time_sum = int(df['Trip Duration'].sum())
    print("Total travel time in seconds:          ", travel_time_sum)
    
    # Convert Seconds To hh:mm:ss:ms
    # solution from https://pynative.com/python-convert-seconds-to-hhmmss/ 
    from datetime import timedelta

    travel_time_sum_converted = timedelta(seconds=travel_time_sum)
    print("Total travel time in days, hh:mm:ss :  ", travel_time_sum_converted)

    # display mean travel time
    travel_time_avg = int(df['Trip Duration'].mean())
    print("Average travel time in seconds:        ", travel_time_avg)
    
    # Convert Seconds To hh:mm:ss:ms
    # solution from https://pynative.com/python-convert-seconds-to-hhmmss/ 

    travel_time_avg_converted = timedelta(seconds=travel_time_avg)
    print("Average travel time in days, hh:mm:ss :", travel_time_avg_converted)
   

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    time.sleep(sleep_sec)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df.groupby('User Type')['User Type'].count()
    print(user_types, "\n")

    # Display counts of gender
    # just for  Chicago and New York City and not for all trips
    try:
        gender_types = df.groupby('Gender')['Gender'].count()
        print(gender_types, "\n")
    except KeyError:
        print("Bikeshare data from Washington contain no information about" 
              "the customer`s gender...")
    
    # Display earliest, most recent, and most common year of birth
    try:
        oldest_cust   = df['Birth Year'].min()
        youngest_cust = df['Birth Year'].max()
        common_cust      = df['Birth Year'].mode()[0]
        print("The oldest   customer was born in",int(oldest_cust))
        print("The youngest customer was born in",int(youngest_cust))
        print("The most common customer was born in",int(common_cust),"\n")
    except KeyError:
        print("... and also no information about the customer`s birth year")
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    time.sleep(sleep_sec)
    
    
def display_raw_data(df):
    """ offering to prompt raw data considering given filter parameters "
        (city, month, day) and prompting this data in junks of 5 rows each. 
        After every junk the user is asked if to proceed. 
        If yes, the next 5 rows are prompted.
        If no, prompting is stopped.
    """
    answer = 'yes'
    counter = 1
    while answer == 'yes':
        answer = input("Do you want to see the next 5 lines of raw data? "
                       "Enter 'yes'or any other key to interupt.\n")
        if answer.lower() != 'yes':
            print("Exit prompting raw data")
            break
        else:
            end = (counter +5) 
            print(df.iloc[counter:end])
            counter += 5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
        restart = input("\nWould you like to restart? "
                        "Enter 'yes' or any other key to interupt.\n")
        if restart.lower() != 'yes':
            print("Good bye!")
            break


if __name__ == "__main__":
	main()



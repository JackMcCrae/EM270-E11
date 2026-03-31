import math

def parse_inputs(file_array):
    #empty array to hold everything
    parsed_data = []
    #loop through all files
    for a in file_array:
        #loop through lines in file
        for b in a:
            #append array of all data in this line to array of entries
            parsed_data.append(b.split(','))
    #loop through each data entry
    for a in len(parsed_data):
        #initially say this entry is valid
        overall_valid = True
        #loop through each field in this data entry
        for b in len(parsed_data[a]):
            #check if this data needs broken down further and if it will cause errors from this knowledge
            checked_value, valid_value = reformat_and_note_errors(parsed_data[a][b], b)
            #check if this section has caused errors, if so update if this data entry overall causes errors
            if valid_value == False:
                overall_valid == False
            #add the seperated data to the array in place of original data
            parsed_data[a][b] = checked_value
        #add section to data entry for if data causes errors, this will continually be updated
        is_valid = [overall_valid]
        parsed_data[a].append(is_valid)
    #return all the seperated values & if they cause errors
    return parsed_data

def run_validation_checks(all_data):
    #loop through all data values
    for a in range(0,len(all_data)):
        #check if data has already been shown to cause problems
        if all_data[a][23] == False:
            #put current data value through validation checker
            all_data[a] = call_validations(all_data[a])
    #return data with error and validation marks
    return(all_data)
            
def reformat_and_note_errors(current_entry, b):
    #attempt to break down certain data points for later use, if an error occurs return that this section is a problem
    try:
        #temporary variables for processing data
        holder_a = []
        holder_b = []
        holder_c = []
        holder_d = []
        #check if data is in start date or end date section
        if b == 0 or b == 2:
            #seperate at a space to have date and time seperate
            holder_a = current_entry.split(' ')
            #break day down int day month and year
            holder_b = holder_a[0].split('/')
            #break time into hour minute and second
            holder_c = holder_a[1].split(':')
            #add date to temporary variable
            for n in range(0,2):
                holder_d[n] = holder_b[n]
            #add on time to temporary variable
            for n in range(3,5):
                holder_d[n] = holder_c[n-3]
            #set value to be returned to value found
            current_entry = holder_d
        #check if data is in start station or end station section
        elif b == 1 or b == 3:
            #break entry to station and area
            current_entry = current_entry.split(',')
        #check if data is in trip category section
        elif b == 7:
            #split at ( to seperate time range on right
            holder_a = current_entry.split('(')
            #split at - to isolate lower time bound
            holder_b = holder_a[1].split('-')
            #split at ) to isolate upper time bound
            holder_c = holder_b[1].split(')')
            #put together array of this data to be returned
            holder_d = [holder_a[0],holder_b[0],holder_c[0]]
            #set array that is returned = to final temperoary array
            current_entry = holder_d
        else:
            #cast current_entry into an array
            current_entry = [current_entry]
        #return data entry and that there have been no errors
        return current_entry, True
    #run if error occurs
    except:
        #cast current_entry into an array
        current_entry = [current_entry]
        #return unchanged entry and that there was an error
        return current_entry, False
    
def check_leap_year(data,field):
    #checking if year is after year 1 AD
    if int(data[field][2] > 0):
        #check if multiple of 4
        if div_error_checker(int(data[field][2],4)) == True:
            #when not a multiple of 4, not a leap year so return False
            return False
        #if it is a multiple of 4, check if it is a multiple of 100
        elif div_error_checker(int(data[field][2]),100) == True:
            #when it is a multiple of 4 and not a multiple of 100 it is a leap yea, so return True
            return True
        #if it is a multiple of 4 and 100, check if it is a multiple of 400
        elif div_error_checker(int(data[field][2]),400) == False:
            #when it is a multiple of 400 it is a leap year, so return True
            return True
    #compensate for lack of year 0, our callendar had no year between 1 BCE/BC and 1 CE/AD by adding 1 to year
    #assumes that year is given in terms of BCE/BC and CE/AD, where a negative value is for BCE/BC and positive is for CE/AD
    #this really isn't necessary
    else:
        print('Why is a value from before the year 1?')
        #check if multiple of 4
        if div_error_checker(int(data[field][2]+1,4)) == True:
            #when not a multiple of 4, not a leap year so return False
            return False
        #if it is a multiple of 4, check if it is a multiple of 100
        elif div_error_checker(int(data[field][2])+1,100) == True:
            #when it is a multiple of 4 and not a multiple of 100 it is a leap year, so return True
            return True
        #if it is a multiple of 4 and 100, check if it is a multiple of 400
        elif div_error_checker(int(data[field][2])+1,400) == False:
            #when it is a multiple of 400 it is a leap year, so return True
            return True

def div_error_checker(numerator,denominator):
    #attempt to divide the numerator by the denominator to find if the numerator is a multiple
    try:
        #divide numerator by denominator
        a = numerator/denominator
        #cast a into an integer, if numerator/denominator is an int numerator is a multiple of denominator, otherwise causes an error
        a = int(a)
        #if no error return False for no error
        return False
    #if there is an error in the above section execute this section
    except:
        #return that there was an error
        return True

def call_validations(current_entry):
    #variable for if data is weird
    dodgy_data = False
    current_entry.append(dodgy_data)
    #data for if variable will cause errors and as such will be removed
    new_error = False
    #checks to run on data. All functions are named as what they will do
    dodgy_data, new_error = check_distance_lat_and_long(current_entry)
    if new_error == True:
        current_entry[23] = new_error
    if dodgy_data == True:
        current_entry[24] = dodgy_data
    dodgy_data, new_error = check_start_hour(current_entry)
    if new_error == True:
        current_entry[23] = new_error
    if dodgy_data == True:
        current_entry[24] = dodgy_data
    dodgy_data, new_error = check_start_month(current_entry)
    if new_error == True:
        current_entry[23] = new_error
    if dodgy_data == True:
        current_entry[24] = dodgy_data
    dodgy_data, new_error = check_trip_duration(current_entry)
    if new_error == True:
        current_entry[23] = new_error
    if dodgy_data == True:
        current_entry[24] = dodgy_data
    dodgy_data, new_error = check_trip_category_with_duration(current_entry)
    if new_error == True:
        current_entry[23] = new_error
    if dodgy_data == True:
        current_entry[24] = dodgy_data
    dodgy_data, new_error = check_if_weekend(current_entry)
    if new_error == True:
        current_entry[23] = new_error
    if dodgy_data == True:
        current_entry[24] = dodgy_data
    dodgy_data, new_error = check_end_date_is_after_start_date(current_entry)
    if new_error == True:
        current_entry[23] = new_error
    if dodgy_data == True:
        current_entry[24] = dodgy_data
    dodgy_data, new_error = check_trip_time_speed_and_distance(current_entry)
    if new_error == True:
        current_entry[23] = new_error
    if dodgy_data == True:
        current_entry[24] = dodgy_data
    dodgy_data, new_error = check_date_exists(current_entry)
    if new_error == True:
        current_entry[23] = new_error
    if dodgy_data == True:
        current_entry[24] = dodgy_data

    return(current_entry)

def remove_big_errors(whole_data_set):
    for i in len(whole_data_set):
        if whole_data_set[i][23] == True:
            whole_data_set.pop(i)
    return whole_data_set


def check_distance_lat_and_long(data):
    try:
        #find change in latitude and longitude from start and end latitude and logitdue in data
        delta_lat = float(data[19][0]) - float(data[17][0])
        delta_long = float(data[20][0]) - float(data[18][0])
        #use havesine formula to find distance around the earth based on these, then check it is >0.9 times the distance and <1.5 times it
        if float(data[21][0]) >= 0.9*6371*2*math.asin(((math.sin(delta_lat/2)**2)+(math.cos(float(data[17][0]))*math.cos(float(data[19][0]))*(math.sin(delta_long/2))**2))**0.5) and float(data[21][0]) <= 1.5*6371*2*math.asin(((math.sin(delta_lat/2)**2)+(math.cos(data[17][0])*math.cos(data[19][0])*(math.sin(delta_long/2))**2))**0.5):
            #if yes, any discrepincies are reasonable, so this isn't dodgy
            return False, False
        else:
            #data is dodgy but doesn't cause errors
            return True, False
    except:
        #data causes errors, don't use it anymore
        return True, True

def check_start_hour(data):
    #attempt comparison
    try:
        #get hour from start date section
        hour_from_date = int(data[0][3])
        #get hour from start hour section
        hour_from_hour = int(data[9][0])
        #check if hours match
        if hour_from_date == hour_from_hour:
            #hours match and cause no erros so return that data is not prpblematic in any way
            return False, False
        else:
            #hours don't match so they're sketchy, but also don't cause a crash. Return this
            return True, False
    #code for if an error occurs
    except:
        #return that the data is odd and that it should not be used in future
        return True, True

def check_start_month(data):
    try:
        #check if month from start_date matches with month from start_month
        #strings starting with a 0 lose it when cast to an int
        if int(data[0][1]) == 1 and data[10][0] == 'Janurary':
            return False, False
        elif int(data[0][1]) == 2 and data[10][0] == 'February':
            return False, False
        elif int(data[0][1]) == 3 and data[10][0] == 'March':
            return False, False
        elif int(data[0][1]) == 4 and data[10][0] == 'April':
            return False, False
        elif int(data[0][1]) == 5 and data[10][0] == 'May':
            return False, False
        elif int(data[0][1]) == 6 and data[10][0] == 'June':
            return False, False
        elif int(data[0][1]) == 7 and data[10][0] == 'July':
            return False, False
        elif int(data[0][1]) == 8 and data[10][0] == 'August':
            return False, False
        elif int(data[0][1]) == 9 and data[10][0] == 'September':
            return False, False
        elif int(data[0][1]) == 10 and data[10][0] == 'October':
            return False, False
        elif int(data[0][1]) == 11 and data[10][0] == 'Novermber':
            return False, False
        elif int(data[0][1]) == 12 and data[10][0] == 'December':
            return False, False
        #if months don't match data is dodgy but doesn't cause an error
        else:
            return True, False
    #if an error occurs then the dta is dodgy and causes an error so return that
    except:
        return True, True
    
def check_trip_duration(data):
    try:
        #check if the start date and end date have the same date
        if data[0][0] == data[2][0] and data[0][1] == data[2][1] and data[0][2] == data[2][2]:
            #find time past 00:00 of trip start, in seconds
            start_time = int(data[0][3])*3600 + int(data[0][4])*60 + int(data[0][5])
            #find time past 00:00 of the trip end, in seconds
            end_time = int(data[2][3])*3600 + int(data[2][4])*60 + int(data[2][5])
            #find time between start and end
            duration = end_time - start_time
            #check if time between start and finish, when converted to minutes, is within a reasonable margin of error of the time listed in the data entry
            if float(duration)/60 <= 1.1*float(data[6][0]) and float(duration) >= 0.9*float(data[6][0]):
                #if it is, no issues with data
                return False, False
            else:
                #otherwise, there are issues with the data but they do not pose a risk of causing a crash
                return True, False
        #check if year and month match
        elif data[0][1] == data[2][1] and data[0][2] == data[2][2]:
            #find the difference in  days, convert it to seconds
            day_related_change_in_time = (int(data[2][0]) - int(data[0][0]))*86400
            #find time past 00:00 on start day of start time
            start_time = int(data[0][3])*3600 + int(data[0][4])*60 + int(data[0][5])
            #find time past 00:00 on start date of end time, using difference in time from difference in days
            end_time = int(data[2][3])*3600 + int(data[2][4])*60 + int(data[2][5]) + day_related_change_in_time
            #use times to find duration
            duration = end_time - start_time
            #convert duration to minutes and check if it is within reasonable margin of error of the time listed in data entry
            if float(duration)/60 <= 1.1*float(data[6][0]) and float(duration) >= 0.9*float(data[6][0]):
                #if it is, no issues with data
                return False, False
            else:
                #otherwise, there are issues with the data but they cause no risk of crashing
                return True, False
        #check if years match
        elif data[0][2] == data[2][2]:
            #if the month is april, june, september or november, handle this with a 30 day long month
            if int(data[0][1]) == 4 or int(data[0][1]) == 6 or int(data[0][1]) == 9 or int(data[0][1]) == 11:
                #set change in time from day/month to position of end day in month - position of start day in month plus length of month times the number of seconds in a day
                day_related_change_in_time = (int(data[2][0]) - int(data[0][0]) + 30)*86400
            #if the month is february handle this using february lengths, including checks for leap years
            elif int(data[0][1] == 2):
                #call check leap year function
                if check_leap_year(data,0) == True:
                    #if it is a leap year use a month length of 29
                    day_related_change_in_time = (int(data[2][0]) - int(data[0][0]) + 29)*86400
                else:
                    #otherwise the length of the month is 28 so use that
                    day_related_change_in_time = (int(data[2][0]) - int(data[0][0]) + 28)*86400
            #all other cases are months with 31 days in it
            else:
                #use a month length of 31 for time change
                day_related_change_in_time = (int(data[2][0]) - int(data[0][0]) + 31)*86400
            #convert to minutes and compare with value from dataset with tollerances
            if float(duration)/60 <= 1.1*float(data[6][0]) and float(duration) >= 0.9*float(data[6][0]):
                return False, False
            else:
                return True, False
    except:
        return True, True
    
def check_trip_category_with_duration(data):
    try:
        #check if trip duration falls within bounds of the trip type
        if float(data[6][0]) >= float(data[7][1]) and float(data[6][0]) <= float(data[7][2]):
            #if it falls within range, no issues
            return False, False
        else:
            #if not say there're issues but not any that'll crash
            return True, False
    except:
        #if things break return that it breaks
        return True, True
    
def check_if_weekend(data):
    try:
        #compare day of week to if 'is_weekend' is high. If high on weekend, return that there are no issues
        if (data[10][0] == 'Saturday' and int(data[12][0]) != 0) or (data[10][0] == 'Sunday' and int(data[12][0]) != 0):
            return False, False
        #otherwise if it is high return that there is an issue
        elif int(data[12][0]) != 0:
            return True, False
        #otherwise all is good
        else:
            return False, False
    except:
        #otherwise mention big issues
        return True, True
    
def check_end_date_is_after_start_date(data):
    try:
        #check if end year is after start year
        #return no issues if it is
        #check if start year is after end year
        #return issues if it is
        #repeat for every denomination of time getting smaller as you go
        if int(data[2][2]) > int(data[0][2]):
            return False, False
        elif int(data[2][2]) < int(data[0][2]):
            return True, False
        elif int(data[2][1]) > int(data[0][1]):
            return False, False
        elif int(data[2][1]) < int(data[0][1]):
            return True, False
        elif int(data[2][0]) > int(data[0][0]):
            return False, False
        elif int(data[2][0]) < int(data[0][0]):
            return True, False
        elif int(data[2][4]) > int(data[0][3]):
            return False, False
        elif int(data[2][4]) < int(data[0][3]):
            return True, False
        elif int(data[2][4]) > int(data[0][4]):
            return False, False
        elif int(data[2][4]) < int(data[0][4]):
            return True, False
        elif int(data[2][5]) > int(data[0][5]):
            return False, False
        elif int(data[2][5]) < int(data[0][5]):
            return True, False
        else:
            return True, False
    except:
        return True, True

def check_trip_time_speed_and_distance(data):
    try:
        #check that the distance found from time and speed is within +50/-10% of the distance listed
        if float(data[6][0])*float(data[22][0]) >= 0.9*float(data[21][0]) and float(data[6][0])*float(data[22][0]) <= 1.5*float(data[21][0]):
            #if it is say we're happy
            return False, False
        else:
            return True, False
    except:
        return True, True

def check_date_exists(data):
    try:
        #check year isn't 0CE/AD or 0BCE/BC as that year doesn't exist
        if int(data[0][2]) == 0 or int(data[2][2]) == 0:
            return True, False
        #check it is one of the 12 months
        elif (int(data[0][1]) <= 12 and int(data[0][1]) >= 1) and (int(data[2][1]) <= 12 and int(data[2][1]) >= 1):
            return False, False
        #check if start month is a month with 30 days
        elif int(data[0][1]) == 4 or int(data[0][1]) == 6 or int(data[0][1]) == 9 or int(data[0][1]) == 11:
            #check if the number of days matches that length
            if int(data[0][0]) < 1 or int(data[0][0]) > 30:
                return True, False
        #check if end month is a month with 30 days
        elif int(data[2][1]) == 4 or int(data[2][1]) == 6 or int(data[2][1]) == 9 or int(data[2][1]) == 11:
            #check if the number of days matches that length
            if int(data[2][0]) < 1 or int(data[2][0]) > 30:
                return True, False
        #check if it is february and the right number of days in february
        elif (int(data[0][1]) == 2 and data[0][0] > 29 and int(data[0][0]) < 1) or (int(data[2][1]) == 2 and data[2][0] > 29 and int(data[21][0]) < 1):
            return True, False
        #check if it is the 29th of february
        elif (int(data[0][0]) == 29 and int(data[0][1]) == 2):
            #check if it is a leap year
            if check_leap_year(data,0) == False:
                return True, False
        elif (int(data[2][0]) == 29 and int(data[2][1]) == 2):
            if check_leap_year(data,2) == False:
                return True, False
        #check if the day falls between the 31st and 1st
        elif int(data[0][0]) > 31 or int(data[0][0]) < 1 or int(data[2][0]) > 31 or int(data[2][0]) < 1:
            return True, False
        #otherwise we're all good
        else:
            return False, False
    except:
        return True, True
    
def remove_error_causing_entries(data):
    #find initial length of array
    b = len(data)
    #loop for initial number of items in array
    for a in range(0, b):
        #going backwards through the array check if this entry contains data that will cause an error
        if data[b-a][23][0] == True:
            #if it does, pop it
            data.pop(b-a)
    #return data that will not cause errors
    return data

def check_unique_stations_and_station_usage_frequency(data):
    #check if start and end stations in initial journey match, if not add both to array of stations
    if data[0][1][0] != data[0][3][0]:
        stations = [data[0][1][0], data[0][3][0]]
        start_station_usage = [1,0]
        end_station_usage = [0,1]
    #if they do match, add start station to array of stations
    else:
        stations = data[0][1][0]
        start_station_usage = [1]
        end_station_usage = [1]
    #loop through every date entry starting at second
    for a in range(1,len(data)):
        #set initial variables to say that start and end stations are not previously visited
        start_match = False
        end_match = False
        #loop through every station that has been visited
        for b in range(0,len(stations)):
            #check if journey started at this station
            if stations[b] == data[a][1][0]:
                #if the start station has been visited before state that start station has been visted before
                start_match = True
                start_station_usage[b] += 1
            #check if journey ended at this station
            if stations[b] == data[a][3][0]:
                #if the end station has been visited before state that the end station has been visited before
                end_match = True
                end_station_usage[b] += 1
            #check if both start and end stations have been visited before
            if start_match == True and end_match == True:
                #stop looping through stations
                break
        #check if start station has been visited
        if start_match == False and end_match == True:
            #if it has not, add it to array of stations
            stations.append(data[a][1][0])
            start_station_usage.append(1)
            end_station_usage.append(0)
        elif start_match == True and end_match == False:
            stations.append(data[a][1][0])
            start_station_usage.append(0)
            end_station_usage.append(1)
        elif start_match == end_match == False:
            if data[a][1][0] == data[a][3][0]:
                stations.append(data[a][1][0])
                start_station_usage.append(1)
                end_station_usage.append(1)
            else:
                stations.append(data[a][1][0], data[a][3][0])
                start_station_usage.append(1,0)
                end_station_usage.append(0,1)
   
    #add the unsorted ones together
    total_station_usage = start_station_usage + end_station_usage

    #sort stations by how many times they are the start station and save as it's own array, as well as number of times started at that station
    start_stations, start_station_usage = bubble_sort_parallel_arrays(start_station_usage, stations)
    #sort stations by how many times they are the end station and save as it's own array, as well as number of times ended at that station
    end_stations, end_station_usage = bubble_sort_parallel_arrays(end_station_usage, stations)
    
    

    #return array of stations visited, number of stations visited and the number of times each station was visited, all sorted
    return len(stations), total_station_usage, stations, start_station_usage, start_stations, end_station_usage, end_stations

def bubble_sort_parallel_arrays(number_array, info_array):
    #set boolean of if the array is sorted to false
    is_sorted = False
    #while array is not sorted
    while is_sorted == False:
        #initially say that the array is sorted
        is_sorted = True
        #loop for thength of array
        for a in range(0,len(number_array)-1):
            #check if value of current array position is greater than next in array of start/end uses
            if number_array[a] > number_array[a+1]:
                #if it is, switch current and next positions in the array of number of occurrences
                number_array[a], number_array[a+1] = number_array[a+1], number_array[a]
                #also switch current and next name in the array of names
                info_array[a], info_array[a+1] = number_array[a+1], number_array[a]
                #say that the arrays are not sorted yet
                is_sorted = False
    #return sorted arrays
    return info_array, number_array

def filter_start_day(data):
    #make empty array for filtered data
    filtered_data = []
    #get day to filter for from user
    chosen_day = str(input('Enter day to filter by: '))
    #loop for number of entries in dataset
    for a in range(0,len(data)):
        #check if day matches day chosen by user using .upper() to remove case sensitivity
        if data[a][10][0].upper() == chosen_day.upper():
            #if it is add it to filtered data array
            filtered_data.append(data[a])
    #return the now filtered data
    return filtered_data

def analyse_filter_data(data):
    #set total journeys equal to number of data entries
    total_journeys = len(data)
    #set minimum trip duration to first duration entry
    minimum_trip_duration = data[0][6][0]
    #set maximum trip ruation to first duration entry
    maximum_trip_duration = data[0][6][0]
    #set total trip duration to first duration entry
    total_trip_duration = data[0][6][0]
    #set minimum trip distance to first distance entry
    minimum_trip_distance = data[0][21][0]
    #set maximum trip distance to first distance entry
    maximum_trip_distance = data[0][21][0]
    #set total trip distance to first distance netry
    total_trip_distance = data[0][21][0]
    #loop for every trip entry but first entry as it has already been entered
    for a in range(1,total_journeys):
        #check for new minimum trip duration
        if data[a][6][0] < minimum_trip_duration:
            #update new minimum
            minimum_trip_duration = data[a][6][0]
        #if not new minimum trip duration, check for new maximum trip duration
        elif data[a][6][0] > maximum_trip_duration:
            #update new maximum
            maximum_trip_duration = data[a][6][0]
        #check for new minim trip distance
        if data[a][21][0] < minimum_trip_distance:
            #update new minimum
            minimum_trip_distance = data[a][21][0]
        #if not new minimum trip distance, check for new maximum trip distance
        elif data[a][21][0] > maximum_trip_distance:
            #update new maximum
            maximum_trip_distance = data[a][21][0]
        #update total duration
        total_trip_duration = total_trip_duration + data[a][6][0]
        #update total distance
        total_trip_distance = total_trip_distance + data[a][21][0]
    #divide total duration by trip number for average trip duration
    average_trip_duration = total_trip_duration/total_journeys
    #divide total distance by trip number for average trip duration
    average_trip_distance = total_trip_distance/total_journeys
    #return total journeys, minimum, maximum and total duration and minim, maximum and total distance
    return total_journeys, minimum_trip_duration, maximum_trip_duration, average_trip_duration, maximum_trip_distance, maximum_trip_distance, average_trip_distance

def open_files():
    files = []
    for a in range(0,int(input("How many files do you want to open? "))):
        files.append(open(str(input('Enter file name and path: ')),'r'))
    return files
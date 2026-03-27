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
    
def check_leap_year(data):
    #checking if year is after year 1 AD
    if int(data[0][2] > 0):
        #check if multiple of 4
        if div_error_checker(int(data[0][2],4)) == True:
            #when not a multiple of 4, not a leap year so return False
            return False
        #if it is a multiple of 4, check if it is a multiple of 100
        elif div_error_checker(int(data[0][2]),100) == True:
            #when it is a multiple of 4 and not a multiple of 100 it is a leap yea, so return True
            return True
        #if it is a multiple of 4 and 100, check if it is a multiple of 400
        elif div_error_checker(int(data[0][2]),400) == False:
            #when it is a multiple of 400 it is a leap year, so return True
            return True
    #compensate for lack of year 0, our callendar had no year between 1 BCE/BC and 1 CE/AD by adding 1 to year
    else:
        #check if multiple of 4
        if div_error_checker(int(data[0][2]+1,4)) == True:
            #when not a multiple of 4, not a leap year so return False
            return False
        #if it is a multiple of 4, check if it is a multiple of 100
        elif div_error_checker(int(data[0][2])+1,100) == True:
            #when it is a multiple of 4 and not a multiple of 100 it is a leap yea, so return True
            return True
        #if it is a multiple of 4 and 100, check if it is a multiple of 400
        elif div_error_checker(int(data[0][2])+1,400) == False:
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
    #data for if variable will cause errors and as such will be removed
    new_error = False
    #checks to run on data. All functions are named as what they will do
    dodgy_data, new_error = check_distance_lat_and_long(current_entry)
    dodgy_data, new_error = check_start_hour(current_entry)
    dodgy_data, new_error = check_start_month(current_entry)
    dodgy_data, new_error = check_trip_duration(current_entry)
    dodgy_data, new_error = check_trip_category_with_duration(current_entry)
    dodgy_data, new_error = check_if_weekend(current_entry)
    dodgy_data, new_error = check_end_date_is_after_start_date(current_entry)
    dodgy_data, new_error = trip_distance_is_real(current_entry)
    dodgy_data, new_error = check_date_exists(current_entry)

    #update if this line causes a major error
    current_entry[23] = new_error
    #add if the data looks dodgy
    current_entry.append(dodgy_data)
    return(current_entry)

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
        if data[0][0] == data[2][0] and data[0][1] == data[2][1] and data[0][2] == data[2][2]:
            start_time = int(data[0][3])*3600 + int(data[0][4])*60 + int(data[0][5])
            end_time = int(data[2][3])*3600 + int(data[2][4])*60 + int(data[2][5])
            duration = end_time - start_time
            if float(duration)/60 <= 1.1*float(data[6][0]) and float(duration) >= 0.9*float(data[6][0]):
                return False, False
            else:
                return True, False
        elif data[0][1] == data[2][1] and data[0][2] == data[2][2]:
            day_related_change_in_time = (int(data[2][0]) - int(data[0][0]))*86400
            start_time = int(data[0][3])*3600 + int(data[0][4])*60 + int(data[0][5])
            end_time = int(data[2][3])*3600 + int(data[2][4])*60 + int(data[2][5]) + day_related_change_in_time
            duration = end_time - start_time
            if float(duration)/60 <= 1.1*float(data[6][0]) and float(duration) >= 0.9*float(data[6][0]):
                return False, False
            else:
                return True, False
        elif data[0][2] == data[2][2]:
            if int(data[0][1]) == 4 or int(data[0][1]) == 6 or int(data[0][1]) == 9 or int(data[0][1]) == 11:
                day_related_change_in_time = (int(data[2][0]) - int(data[0][0]) + 30)*86400
            elif data[0][1] == 2:
                if check_leap_year(data) == True:

            else:
                day_related_change_in_time = (int(data[2][0]) - int(data[0][0]) + 31)*86400
        


    except:
        return True, True
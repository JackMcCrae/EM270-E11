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
            checked_value, valid_value = check_data_validity_and_reformat(parsed_data[a][b], b)
            #check if this section has caused errors, if so update if this data entry overall causes errors
            if valid_value == False:
                overall_valid == False
            #add the seperated data to the array in place of original data
            parsed_data[a][b] = checked_value
        #add section to data entry for if data causes errors, this will continually be updated
        if overall_valid == True:
            parsed_data[a].append(True)
        else:
            parsed_data[a].append(False)
    #return all the seperated values & if they cause errors
    return parsed_data

            
def check_data_validity_and_reformat(current_entry, b):
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
        #return data entry and that there have been no errors
        return current_entry, True
    #run if error occurs
    except:
        #return unchanged entry and that there was an error
        return current_entry, False
    
def check_leap_year(year):
    #check if multiple of 4
    if div_error_checker(year,4) == True:
        #when not a multiple of 4, not a leap year so return False
        return False
    #if it is a multiple of 4, check if it is a multiple of 100
    elif div_error_checker(year,100) == True:
        #when it is a multiple of 4 and not a multiple of 100 it is a leap yea, so return True
        return True
    #if it is a multiple of 4 and 100, check if it is a multiple of 400
    elif div_error_checker(year,400) == False:
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
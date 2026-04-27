
def filter_by_distance(data, min_distance):
    return [
        record for record in data
        if float(record.get("trip_distance_km", 0)) >= min_distance
        ]

def filter_by_timerange(data, start_hour, end_hour):
    return [
        record for record in data
        if start_hour <= int(record.get("start_hour", -1)) <= end_hour
        ]

def filter_by_endhour(data, hour):
    return [
        record for record in data
        if int(record.get("start_hour", -1)) == hour
        ]

def apply_filters(data):
    print("\n--- FILTER OPTIONS ---")
    print("1. Minimum journey distance")
    print("2. Start time range")
    print("3. Specific start hour")
    print("4. No filter")
    
    choice = input("Choose filter option: ")
    
    if choice == "1":
        min_d = float(input("Enter minimum distance (km): "))
        return filter_by_distance(data, min_d)
    
    elif choice == "2":
        start = int(input("Enter start hour (0-23): "))
        end = int(input("Enter end hour (0-23): "))
        return filter_by_timerange(data, start, end)
    
    elif choice == "3":
        hour = int(input("Enter hour (0-23): "))
        return filter_by_endhour(data, hour)
    
    elif choice == "4":
        return data
    
    else:
        print("Invalid choice -  no filter applied.")
        return data
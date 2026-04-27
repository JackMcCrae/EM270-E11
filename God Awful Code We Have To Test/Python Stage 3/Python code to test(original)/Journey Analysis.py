def analyse_journeys_by_day(data, day):
    # Lists to store values
    durations = []
    distances = []

   # Filter records for the selected day
   #Loops through every journey record to convert values to lowercase avoiding case errors and builds a new list only containing matchibng journeys
    for record in data:
        # Check if day matches correctly 
        if record['start_day'].lower() == day.lower():
            try:
              
                duration = float(record['duration_min'])
                distance = float(record['trip_distance_km'])

                durations.append(duration)
                distances.append(distance)

            except:
                # Skip bad data
                continue

  # handle case where no data is found in system
  # this section prevents a crash in the system when trying to calculate stats using an empty list instead presents message 
    if len(durations) == 0:
        print("No data found for that day.")
        return

    # calculate statistics
    # this takes a list of numbers and summarises them using the min,max and average values
    total = len(durations)
    min_dur = min(durations)
    max_dur = max(durations)
    avg_dur = sum(durations) / total
    min_dist = min(distances)
    max_dist = max(distances)
    avg_dist = sum(distances) / total

    # Print results
    #displays the results in clear understandable user friendly way
    print("\nResults for", day)
    print("Total journeys:", total)
    print("\nDuration (mins):")
    print("Min:", min_dur)
    print("Max:", max_dur)
    print("Average:", round(avg_dur, 2))
    print("\nDistance (km):")
    print("Min:", min_dist)
    print("Max:", max_dist)
    print("Average:", round(avg_dist, 2))
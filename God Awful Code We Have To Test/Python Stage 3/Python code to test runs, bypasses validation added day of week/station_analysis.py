
import csv
from collections import Counter


def analyse_stations(valid_records):
    start_counts = Counter()
    end_counts = Counter()
    unique_stations = set()

    for record in valid_records:
        start_station = str(record.get("start_station", "")).strip()
        end_station = str(record.get("end_station", "")).strip()
        
        if start_station != "":
            start_counts[start_station] += 1
            unique_stations.add(start_station)

        if end_station != "":
            end_counts[end_station] += 1
            unique_stations.add(end_station)

    results = {
        "total_unique_stations": len(unique_stations),
        "top_3_start": start_counts.most_common(3),
        "top_3_end": end_counts.most_common(3),
        "start_counts": start_counts,
        "end_counts": end_counts,
        "unique_stations": sorted(unique_stations)
    }

    return results


def display_station_analysis(results):
 
    print("Station Analysis")
    print("Total number of unique stations:",
          results["total_unique_stations"])

    print("Three most frequently used starting stations:")
    if len(results["top_3_start"]) == 0:
        print("No starting station data found.")
    else:
        rank = 1
        for station, count in results["top_3_start"]:
            print(str(rank) + ".", station, "-", count, "trips")
            rank += 1

    print("Three most frequently used ending stations:")
    if len(results["top_3_end"]) == 0:
        print("No ending station data found.")
    else:
        rank = 1
        for station, count in results["top_3_end"]:
            print(str(rank) + ".", station, "-", count, "trips")
            rank += 1


def write_stations_csv(results, filename="stations.csv"):
  
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Stations", "Start", "End"])

        for station in results["unique_stations"]:
            start_total = results["start_counts"].get(station, 0)
            end_total = results["end_counts"].get(station, 0)
            writer.writerow([station, start_total, end_total])

    print("Station data has been written to", filename)


def station_analysis_menu(valid_records):

    results = analyse_stations(valid_records)
    display_station_analysis(results)

    choice = input("Do you want to save station results to stations.csv? (yes/no): ")

    if choice == "yes":
        write_stations_csv(results)
    else:
        print("stations.csv was not created.")
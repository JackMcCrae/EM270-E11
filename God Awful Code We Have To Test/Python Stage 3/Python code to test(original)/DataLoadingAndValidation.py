import csv
from datetime import datetime
import math

# HAVERSINE FUNCTION

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # km

    # convert to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c

# LOAD CSV FILES

def load_files():
    print("Enter CSV filenames separated by commas:")
    filenames = input("Files: ").split(",")

    all_records = []

    for name in filenames:
        name = name.strip()
        try:
            with open(name, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    all_records.append(row)
            print("Loaded:", name)
        except:
            print("Could not open:", name)

    return all_records

# VALIDATE RECORDS

def validate(records):
    cleaned = []
    suspects = []

    for r in records:
        reason = ""

        # Check required fields
        
        required = ["start_date", "end date", "duration_min",
                    "trip distance km", "start lat _", "start_long",
                    "end lat", "end long"]

        for field in required:
            if r.get(field, "").strip() == "":
                reason = "Missing field: " + field

        if reason != "":
            r["reason"] = reason
            suspects.append(r)
            continue

        # Convert values
        
        try:
            start = datetime.strptime(r["start_date"], "%d/%m/%Y %H:%M:%S")
            end = datetime.strptime(r["end date"], "%d/%m/%Y %H:%M:%S")
            duration_actual = (end - start).total_seconds() / 60
            duration_recorded = float(r["duration_min"])
        except:
            r["reason"] = "Invalid date or duration format"
            suspects.append(r)
            continue

        # Duration checks
        
        if duration_actual <= 0:
            reason = "Duration <= 0"
        if abs(duration_actual - duration_recorded) > 1:
            reason = "Duration mismatch"

        # Distance checks
        
        try:
            lat1 = float(r["start lat _"])
            lon1 = float(r["start_long"])
            lat2 = float(r["end lat"])
            lon2 = float(r["end long"])
            dist = float(r["trip distance km"])
        except:
            r["reason"] = "Invalid coordinate or distance"
            suspects.append(r)
            continue

        hav_dist = haversine(lat1, lon1, lat2, lon2)

        if dist < hav_dist:
            reason = "Distance smaller than haversine"
        if dist > 3 * hav_dist:
            reason = "Distance too large"

        # Speed check
        
        if duration_actual > 0:
            speed = dist / (duration_actual / 60)
            if speed < 2:
                reason = "Speed < 2 km/h"
            if speed > 40:
                reason = "Speed > 40 km/h"

        # Final decision
        
        if reason != "":
            r["reason"] = reason
            suspects.append(r)
        else:
            cleaned.append(r)

    return cleaned, suspects

# SAVE SUSPECTS 

def save_suspects(suspects):
    if len(suspects) == 0:
        print("No suspect records.")
        return

    with open("suspect_records.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=suspects[0].keys())
        writer.writeheader()
        writer.writerows(suspects)

    print("Saved suspect_records.csv")

# MAIN FUNCTION

def load_and_validate():
    records = load_files()
    cleaned, suspects = validate(records)

    print("\nTotal records:", len(records))
    print("Suspect records:", len(suspects))

    if len(records) > 0:
        percent = (len(suspects) / len(records)) * 100
        print("Percentage suspect:", round(percent, 2), "%")

    save_suspects(suspects)

    return cleaned

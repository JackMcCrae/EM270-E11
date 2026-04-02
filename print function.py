#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 21:00:05 2026

@author: fraserwilkie
"""

def print_filtered_data(data):
    print("\n========== PROCESSED DATA ==========\n")

    for i, entry in enumerate(data):
        print(f"Entry {i+1}")
        
        print("Total Number of Journeys: ", total_journeys)
        print("Minimum Journey Duration: ", minimum_trip_duration)
        print("Maximum Journey Duration: ", maximum_trip_duration)
        print("Average Journey Duration: ", average_trip_duration)
        print("Miniimum Trip Distance: ", minimum_trip_distance)
        print("Maxiimum Trip Distance: ", maximum_trip_distance)
        print("Average Trip Distance:", average_trip_distance)
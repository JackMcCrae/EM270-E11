
from filtering import apply_filters
from station_analysis import station_analysis_menu

def display_menu():
    print("\n--- BIKE DATA ANALYSIS ---")
    print("1. Station Usage Analysis")
    print("2. Exit")
    
def main_interface(valid_records):
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        
        if choice == "1":
            print("\nApply a filter before analysis?")
            use_filter = input("yes/no: ").lower()
            
            if use_filter == "yes":
                filtered_records = apply_filters(valid_records)
            else:
                filtered_records = valid_records
                
            station_analysis_menu(filtered_records)

        elif choice == "2":
            print("Exiting program.")
            break
        
        else:
            print("Invalid option. Try again.")
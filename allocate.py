import pandas as pd

data_dir = "data/"
# Load boat and section data from Excel sheet
boat_data = pd.read_excel(data_dir + "boat_data.xlsx", sheet_name="boats")
section_data = pd.read_excel(data_dir + "boat_data.xlsx", sheet_name="sections")

# Group boats by length
boats_by_length = {}
for _, row in boat_data.iterrows():
    boat_length = row["length"]
    if boat_length not in boats_by_length:
        boats_by_length[boat_length] = []
    boats_by_length[boat_length].append(row)

# Sort boat groups by length in descending order
boat_groups = sorted(boats_by_length.values(), key=lambda group: group[0]["length"], reverse=True)

# Sort sections by length in descending order
sections = section_data.sort_values("length", ascending=False).to_dict("records")

# Define interspace constants
small_boat_width = 2.8
interspace_small_boats = 0.25
interspace_large_boats = 0.4

# Define functions for checking if a boat fits in a section
def fits_in_section(boat, section):
    max_width = section["length"] - interspace_large_boats
    if boat["width"] <= small_boat_width:
        max_width = section["length"] - interspace_small_boats
    if boat["width"] > max_width:
        return False
    return True

def fits_in_buoy(boat, buoy):
    if boat["weight"] > buoy["capacity"]:
        return False
    return True

# Allocate boats to sections and buoys
allocated_boats = {section["name"]: {i: [] for i in range(section["buoys"])} for section in sections}
for boat_group in boat_groups:
    for boat in boat_group:
        for section in sections:
            if fits_in_section(boat, section):
                for i in range(section["buoys"]):
                    if fits_in_buoy(boat, section["buoy_capacities"][i]):
                        allocated_boats[section["name"]][i].append(boat)
                        section["buoy_capacities"][i]["capacity"] -= boat["weight"]
                        break

# Print allocation results
for section in sections:
    print(f"Section {section['name']}:")
    for i in range(section["buoys"]):
        print(f"  Buoy {i+1}:")
        for boat in allocated_boats[section["name"]][i]:
            print(f"    {boat['name']}")
def allocate_boats(boat_data, section_data, max_weight_diff, max_length_diff, max_freeboard_diff, prefer_wooden):
    # Sort the boats by length (ascending) and weight (descending).
    sorted_boats = sorted(boat_data, key=lambda x: (x[0], -x[3]))

    # Define a function to calculate the required interspace between boats.
    def interspace_needed(boat_width):
        if boat_width <= 2.8:
            return 0.25
        else:
            return 0.4

    # Initialize the allocation list.
    allocated_boats = []

    # Allocate the boats to sections.
    for section in section_data:
        section_length = section[0]
        section_buoy_capacity = section[1]
        section_buoy_count = section[2]
        available_buoy_capacity = section_buoy_capacity * section_buoy_count
        allocated_boats_in_section = []

        for boat in sorted_boats:
            boat_length, boat_width, boat_depth, boat_weight, boat_material = boat

            # Skip wooden boats if they are not preferred in this section.
            if boat_material == 'wood' and not prefer_wooden:
                continue

            # Check if the boat fits in the section.
            interspace = interspace_needed(boat_width)
            if boat_width + interspace > section_length:
                continue

            # Check if the boat exceeds the individual buoy capacity.
            if boat_weight > section_buoy_capacity:
                continue

            # Check if the boat fits next to the previously allocated boats.
            if len(allocated_boats_in_section) > 0:
                prev_boat = allocated_boats_in_section[-1]
                prev_boat_length, prev_boat_width, prev_boat_depth, _, _ = prev_boat

                # Check length difference
                length_diff = abs(boat_length - prev_boat_length)
                if length_diff > max_length_diff:
                    continue

                # Check weight difference
                weight_diff = abs(boat_weight - prev_boat[3])
                if weight_diff > max_weight_diff:
                    continue

                # Check freeboard height difference
                freeboard_diff = abs(boat_depth - prev_boat_depth)
                if freeboard_diff > max_freeboard_diff:
                    continue

            # Allocate the boat to the section.
            allocated_boats_in_section.append(boat)
            available_buoy_capacity -= boat_weight
            if available_buoy_capacity < 0:
                break

        # Append the allocated boats and section to the result.
        allocated_boats.extend([(boat, section) for boat in allocated_boats_in_section])

    return allocated_boats

def parse_inputs_check_validity(file_array):
    #finding inputs
    parsed_data = []
    for a in file_array:
        current_file = []
        for b in a:
            current_file.append(b)
        parsed_data.append(current_file)
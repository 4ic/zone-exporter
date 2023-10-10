# This code is a collaboration between a graphic designer and a chatbot. If it works, it's a design miracle. If not, well... you were warned!

import csv
import os
from collections import defaultdict

def clear_directory(directory):
    """Delete all files and subdirectories within the given directory."""
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

# Create the export folder if it does not exist
if not os.path.exists('export'):
    os.makedirs('export')
else:
    # Clear the contents of the 'export' folder
    clear_directory('export')

# Get all files in the 'import' folder
files = os.listdir('import')

for filename in files:
    if filename.endswith('.csv'):
        # Create a folder for each CSV file within the 'export' folder
        folder_name = filename.rsplit('.', 1)[0]
        export_folder = os.path.join('export', folder_name)
        if not os.path.exists(export_folder):
            os.makedirs(export_folder)

        # Read the CSV file
        with open(os.path.join('import', filename), 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row

            # Create dictionaries to store postcodes and prices for General and Variable zones
            general = defaultdict(list)
            variable_suburb = defaultdict(list)
            variable_postcode = defaultdict(list)
            excluded = []

            # Create a dictionary to store the count of each suburb name
            name_count = defaultdict(int)

            # Create a list to store all the rows
            rows = []

            for row in reader:
                postcode, name, price = row
                name_count[name] += 1
                rows.append(row)

            for row in rows:
                postcode, name, price = row
                if float(price) > 200:
                    excluded.append(f'{name} ({postcode})')
                elif name_count[name] == 1:
                    general[price].append(name)
                else:
                    variable_suburb[price].append(name)
                    variable_postcode[price].append(postcode)

            # When writing the results, save them in the new folder
            for price, names in general.items():
                price_int = int(float(price))
                with open(os.path.join(export_folder, f'{price_int}-general.txt'), 'w') as file:
                    file.write('|'.join(names) + '|')

            for price, names in variable_suburb.items():
                price_int = int(float(price))
                with open(os.path.join(export_folder, f'{price_int}-variable-suburb.txt'), 'w') as file:
                    file.write('|'.join(names) + '|')

            for price, postcodes in variable_postcode.items():
                price_int = int(float(price))
                with open(os.path.join(export_folder, f'{price_int}-variable-postcode.txt'), 'w') as file:
                    file.write('|'.join(postcodes) + '|')

            with open(os.path.join(export_folder, 'excluded.txt'), 'w') as file:
                file.write(', '.join(excluded))

            with open(os.path.join(export_folder, 'log.txt'), 'w') as file:
                for price in sorted(set(general.keys()) | set(variable_suburb.keys()), key=float):
                    general_names = general.get(price, [])
                    variable_names = variable_suburb.get(price, [])
                    if general_names:
                        file.write(f'{price} General zones: {len(general_names)}\n')
                    if variable_names:
                        file.write(f'{price} Variable zones: {len(variable_names)}\n')
                file.write(f'Excluded zones: {len(excluded)}\n')
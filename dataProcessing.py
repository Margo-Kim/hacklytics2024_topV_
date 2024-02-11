# this file is used to process the data from the JSON file and output the data to a text file

import json

# The path to your JSON file
file_path = "ticker_data_results.json"

# Open and load the JSON data
with open(file_path, 'r') as file:
    data = json.load(file)

# Assuming 'data' is a dictionary, extract key values
# Example: Extracting a specific value
# if 'your_key_here' in data:
#     value = data['your_key_here']
#     print(f"The value of 'your_key_here' is: {value}")
# else:
#     print("Key not found.")

outputFile = open('output.txt', 'w', encoding='utf-8')
companyDescription = {}
# If you want to iterate over all key-value pairs
for key, value in data.items():
    # output = data[key]["general_info"]["description"]
    companyDescription[key] = data[key]["general_info"]["description"]
    outputFile.write(key + "\t" + companyDescription[key] + "\n")

outputFile.close()

import xml.etree.ElementTree as ET
import json
import os
import re

# Set folder locations for XML input, JSON output, and merged intermediate XML files
xml_folder = 'E:\\Documents\\Education\\PG University of Birmingham\\MSc Computer Science\\Summer Semester\\MSc Projects\\Project Files\\Dataset\\test\\xml'
# json_output_folder = 'E:\\Documents\\Education\\PG University of Birmingham\\MSc Computer Science\\Summer Semester\\MSc Projects\\Project Files\\Dataset\\json' 
merged_xml_folder = 'E:\\Documents\\Education\\PG University of Birmingham\\MSc Computer Science\\Summer Semester\\MSc Projects\\Project Files\\Dataset\\test\\merged'

# Define filename date regular expression pattern
date_pattern = r'\d{4}-\d{2}-\d{2}'

# Check whether the input and output folders exist
os.makedirs(xml_folder, exist_ok=True)
# os.makedirs(json_output_folder, exist_ok=True)

# Create a list of lists of XML files that share the same date
previous_matching_files = []
merge_list = []
for xml_file in os.listdir(xml_folder):
    match = re.search(date_pattern, xml_file)
    matching_files = [xml_file for xml_file in os.listdir(xml_folder) if match.group() in xml_file]
    if matching_files != previous_matching_files:
        merge_list.append(matching_files)
    previous_matching_files = matching_files
print(merge_list)

# Merge data from XML files in each merge_list index in a new XML file
for files in merge_list:
    match = re.search(date_pattern, files[0])
    merged_root = ET.Element("merged_data" + match.group())
    for xml_file in files:
        xml_path = os.path.join(xml_folder, xml_file)
        with open(xml_path, "r", encoding="UTF-8") as file:
            xml_data = file.read()
            root = ET.fromstring(xml_data)
            
            for element in root:
                merged_root.append(element)
                
    merged_file = ET.ElementTree(merged_root)
    merged_file.write(merged_xml_folder + "\\merged" + match.group() + ".xml")
            
# Parse XML data 
# for xml_file in os.listdir(xml_folder):
#     if xml_file.endswith('.xml'):
#         xml_path = os.path.join(xml_folder, xml_file)
#         json_filename = os.path.splitext(xml_file)[0] + '.json'
#         json_path = os.path.join(json_output_folder, json_filename)
        
#         tree = ET.parse(xml_path)
#         root = tree.getroot()
        
#         data = []
        
#         # Iterates through each element, collating any text speech content
#         for element in root:
#             item = {}
#             for sub_element in element:
#                 item[sub_element.tag] = sub_element.text
#             if item != {}:
#                 data.append(item)
        
#         # Adds the collected data to the .json file
#         with open(json_path, 'w') as json_file:
#             json.dump(data, json_file, indent=4)
import xml.etree.ElementTree as ET
import json
import os

# Set folder locations for XML input and JSON output
xml_folder = 'E:\\Documents\\Education\\PG University of Birmingham\\MSc Computer Science\\Summer Semester\\MSc Projects\\Project Files\\Dataset\\xml'
json_output_folder = 'E:\\Documents\\Education\\PG University of Birmingham\\MSc Computer Science\\Summer Semester\\MSc Projects\\Project Files\\Dataset\\json' 

# Check whether the input and output folders exist
os.makedirs(xml_folder, exist_ok=True)
os.makedirs(json_output_folder, exist_ok=True)

# Parse XML data 
for xml_file in os.listdir(xml_folder):
    if xml_file.endswith('.xml'):
        xml_path = os.path.join(xml_folder, xml_file)
        json_filename = os.path.splitext(xml_file)[0] + '.json'
        json_path = os.path.join(json_output_folder, json_filename)
        
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        data = []
        
        # Iterates through each element, collating any text speech content
        for element in root:
            item = {}
            for sub_element in element:
                item[sub_element.tag] = sub_element.text
            if item != {}:
                data.append(item)
        
        # Adds the collected data to the .json file
        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
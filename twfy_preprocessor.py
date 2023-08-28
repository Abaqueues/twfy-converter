import xml.etree.ElementTree as ET
import json
import os
import re

# Set folder locations for XML input, JSON output, and merged intermediate XML files
xml_folder = 'E:\\Documents\\Education\\PG University of Birmingham\\MSc Computer Science\\Summer Semester\\MSc Projects\\Project Files\\Dataset\\final\\xml'
json_output_folder = 'E:\\Documents\\Education\\PG University of Birmingham\\MSc Computer Science\\Summer Semester\\MSc Projects\\Project Files\\Dataset\\final\\json' 
merged_xml_folder = 'E:\\Documents\\Education\\PG University of Birmingham\\MSc Computer Science\\Summer Semester\\MSc Projects\\Project Files\\Dataset\\final\\merged'

# Check whether the input and output folders exist
os.makedirs(xml_folder, exist_ok=True)
# os.makedirs(json_output_folder, exist_ok=True)

# Define filename date regular expression pattern
date_pattern = r'\d{4}-\d{2}-\d{2}'

# Create a list of lists of XML files that share the same date
def match_file_dates():
    previous_matching_files = []
    merge_list = []
    for xml_file in os.listdir(xml_folder):
        match = re.search(date_pattern, xml_file)
        matching_files = [xml_file for xml_file in os.listdir(xml_folder) if match.group() in xml_file]
        if matching_files != previous_matching_files:
            merge_list.append(matching_files)
        previous_matching_files = matching_files
    print("Files to merge:", *merge_list, sep = "\n- ")
    return merge_list

# Merge data from XML files in each merge_list index in a new XML file
def merge_xml_data(file_list):
    merged_file_list = []
    for files in file_list:
        print(files)
        match = re.search(date_pattern, files[0])
        merged_root = ET.Element("merged_data" + match.group())
        for xml_file in files:
            xml_path = os.path.join(xml_folder, xml_file)
            with open(xml_path, "r", encoding="unicode_escape") as file:
                xml_data = file.read()
                root = ET.fromstring(xml_data)
                for element in root:
                    merged_root.append(element)           
        merged_file = ET.ElementTree(merged_root)
        merged_file.write(merged_xml_folder + "\\merged" + match.group() + ".xml")
        merged_file_list.append("merged" + match.group() + ".xml")
    # print("\nMerged files:", *merged_file_list, sep = "\n- ")
        
merge_xml_data(match_file_dates())

# Function to check whether an XML file contains a division
def contains_division(xml_file):
    tree = ET.parse(merged_xml_folder + "\\" + xml_file)
    root = tree.getroot()
    element = root.find("division")
    if element is not None:
        return True
    else:
        return False

# Function that returns a list of files containing a division
def report_division_files(): 
    division_true_list = []
    division_false_list = []
    for file in os.listdir(merged_xml_folder):
        if contains_division(file):
            division_true_list.append(file)
        else:
            division_false_list.append(file)
    # print("\nFiles containing division:", *division_true_list, sep = "\n- ")
    # print("\nFiles missing division:", *division_false_list, sep = "\n- ")
    return division_true_list

# Function that assigns division vote labels to XML speech tags
def assign_vote_labels(file_list):
    for file in file_list:
        print(file)
        divisions = {}
        tree = ET.parse(merged_xml_folder + "\\" + file)
        root = tree.getroot()
        for division in root.iter("division"):
            match = re.search(r'\b(\d{4}-\d{2}-\d{2}[a-zA-Z]?)\b', division.attrib["id"])
            divisions.update({match.group(1) : division})
            mplist = division.findall("mplist")
            for list in mplist:
                mps_votes = {}
                mps_votes.update({"division_id" : match.group(1)})
                for mp in list.findall("mpname"):
                    mps_votes.update({mp.attrib["person_id"] : mp.attrib["vote"]})
                for speech in root.iter("speech"):
                    match = re.search(r'\b(\d{4}-\d{2}-\d{2}[a-zA-Z]?)\b', speech.attrib["id"])
                    if mps_votes["division_id"] == match.group() and "person_id" in speech.attrib:
                        if speech.attrib["person_id"] in mps_votes:
                            mp_vote = mps_votes[speech.attrib["person_id"]]
                            speech.set("vote", mp_vote)        
        
        # Iterates through each element, collating any text speech content
        match = re.search(r'\d{4}-\d{2}-\d{2}', file)
        json_filename = match.group(0) + ".json"
        json_path = os.path.join(json_output_folder, json_filename)
        
        data = []
        
        for element in root:
            if element.tag in ["speech"] and "person_id" in element.attrib:
                item = {}
                for sub_element in element:
                    item[sub_element.tag] = sub_element.text
                element_data = {
                    "tag": element.tag,
                    "attributes": element.attrib,
                    "text": item
                }
                data.append(element_data)
                
        # Adds the collected data to the .json file
        json_data = json.dumps(data, indent=4)
        with open(json_path, "w") as file:
            file.write(json_data)
            print(json_path)
            
assign_vote_labels(report_division_files())

         
            
# def convert_unicode():
#     for file in os.listdir(json_output_folder):
#         json_path = os.path.join(json_output_folder, file)
#         with open(json_path, 'r+', encoding='utf-8') as json_file:
#             json_data = json_file.read()
#             # decoded_text = json_data.encode('utf-8').decode('\u2019')
#             decoded_text = json_data.replace('\u2019', '\'')
#         with open(json_path, 'w', encoding='utf-8') as json_file:
#             json_file.write(decoded_text)

# Parse merged XML data 
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
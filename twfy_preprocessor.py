import xml.etree.ElementTree as ET
import json
import os
import re

# Set folder locations for XML input, JSON output, and merged intermediate XML files
_XML_FOLDER = 'E:\\Documents\\Education\\PG University of Birmingham\\MSc Computer Science\\Summer Semester\\MSc Projects\\Project Files\\Dataset\\final\\xml'
_JSON_OUTPUT_FOLDER = 'E:\\Documents\\Education\\PG University of Birmingham\\MSc Computer Science\\Summer Semester\\MSc Projects\\Project Files\\Dataset\\final\\json' 
_MERGED_XML_FOLDER = 'E:\\Documents\\Education\\PG University of Birmingham\\MSc Computer Science\\Summer Semester\\MSc Projects\\Project Files\\Dataset\\final\\merged'

# Check whether the input and output folders exist
os.makedirs(_XML_FOLDER, exist_ok=True)
# os.makedirs(_JSON_OUTPUT_FOLDER, exist_ok=True)

# Define filename date regular expression pattern
_DATE_PATTERN = r'\d{4}-\d{2}-\d{2}'

# Create a list of lists of XML files that share the same date
def match_file_dates():
    previous_matching_files = []
    merge_list = []
    for xml_file in os.listdir(_XML_FOLDER):
        match = re.search(_DATE_PATTERN, xml_file)
        matching_files = [xml_file for xml_file in os.listdir(_XML_FOLDER) if match.group() in xml_file]
        if matching_files != previous_matching_files:
            merge_list.append(matching_files)
        previous_matching_files = matching_files
    # print("Files to merge:", *merge_list, sep = "\n- ")
    return merge_list

# Merge data from XML files in each merge_list index in a new XML file
def merge_xml_data(file_list):
    merged_file_list = []
    for files in file_list:
        match = re.search(_DATE_PATTERN, files[0])
        merged_root = ET.Element("merged_data" + match.group())
        for xml_file in files:
            xml_path = os.path.join(_XML_FOLDER, xml_file)
            with open(xml_path, "r", encoding="unicode_escape") as file:
                xml_data = file.read()
                root = ET.fromstring(xml_data)
                for element in root:
                    merged_root.append(element)           
        merged_file = ET.ElementTree(merged_root)
        merged_file.write(_MERGED_XML_FOLDER + "\\merged" + match.group() + ".xml")
        merged_file_list.append("merged" + match.group() + ".xml")
    # print("\nMerged files:", *merged_file_list, sep = "\n- ")

# Function to check whether an XML file contains a division
def contains_division(xml_file):
    tree = ET.parse(_MERGED_XML_FOLDER + "\\" + xml_file)
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
    for file in os.listdir(_MERGED_XML_FOLDER):
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
        tree = ET.parse(_MERGED_XML_FOLDER + "\\" + file)
        root = tree.getroot()
        for division in root.iter("division"):
            match = re.search(r'\b(\d{4}-\d{2}-\d{2}[a-zA-Z]?)\b', division.attrib["id"])
            divisions.update({match.group(1) : division})
            mplist = division.findall("mplist")
            for list in mplist:
                mps_votes = {}
                mps_votes.update({"division_id" : match.group(1)})
                for mp in list.findall("mpname"):
                    if "id" in mp.attrib:
                        mp.set("person_id", mp.attrib["id"])
                        del mp.attrib["id"]
                    mps_votes.update({mp.attrib["person_id"] : mp.attrib["vote"]})
                for speech in root.iter("speech"):
                    match = re.search(r'\b(\d{4}-\d{2}-\d{2}[a-zA-Z]?)\b', speech.attrib["id"])
                    if mps_votes["division_id"] == match.group() and ("person_id" in speech.attrib or "speakerid" in speech.attrib):
                        if "speakerid" in speech.attrib:
                            speech.set("person_id", speech.attrib["speakerid"])
                            del speech.attrib["speakerid"]
                        if speech.attrib["person_id"] in mps_votes:
                            mp_vote = mps_votes[speech.attrib["person_id"]]
                            speech.set("vote", mp_vote)        
        
        # Iterates through each element, collating any text speech content in a JSON format
        match = re.search(_DATE_PATTERN, file)
        json_filename = match.group(0) + ".json"
        json_path = os.path.join(_JSON_OUTPUT_FOLDER + "\\", json_filename)
        data = []
        for element in root:
            if element.tag in ["speech"] and ("person_id" in element.attrib or "speakerid" in element.attrib):
                item = {}
                if "speakerid" in element.attrib:
                    element.set("person_id", element.attrib["speakerid"])
                    del element.attrib["speakerid"]
                if "vote" in element.attrib:
                    for sub_element in element:
                            item[sub_element.tag] = sub_element.text
                    element_data = {
                        "tag": element.tag,
                        "attributes": element.attrib,
                        "text": item
                    }
                    data.append(element_data)
                
        # Writes the collected data to the JSON file
        json_data += json.dumps(speech, indent=4)
        with open(json_path, "w", encoding="utf-8") as file:
            file.write(json_data)
            
# merge_xml_data(match_file_dates())
assign_vote_labels(report_division_files())
import os
import json
import csv
from bs4 import BeautifulSoup

# Define paths
csv_file_path = "data_labeling.csv"
data_folder_path = "data"  # Adjust this path to the correct folder containing the data

# Function to extract title and meta tags from an HTML string
def extract_tags_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract the full <title> tag as a string
    title_tag = str(soup.title) if soup.title else "No title found"
    
    # Extract all <meta> tags as full strings, or return an empty string if none are found
    meta_tags_list = [str(meta) for meta in soup.find_all('meta')]
    meta_tags = "\n".join(meta_tags_list) if meta_tags_list else ""
    
    return title_tag, meta_tags

# Function to check if a file contains valid JSON
def is_valid_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            json.load(file)
        return True
    except (json.JSONDecodeError, UnicodeDecodeError):
        return False

# Read and update the CSV
with open(csv_file_path, "r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    rows = list(reader)

    # Ensure "Title tag" and "Meta tags" columns exist, otherwise add them
    fieldnames = reader.fieldnames
    if "Title tag" not in fieldnames:
        fieldnames.append("Title tag")
    if "Meta tags" not in fieldnames:
        fieldnames.append("Meta tags")

# Process each row in order
for index, row in enumerate(rows):
    folder_name = row["Name of Folder"]
    folder_path = os.path.join(data_folder_path, folder_name)
    print(f"Processing folder: {folder_name}")

    # Check if the corresponding folder exists
    if os.path.isdir(folder_path):
        # Look for the 'pages' subfolder
        pages_folder_path = os.path.join(folder_path, 'pages')
        if os.path.exists(pages_folder_path) and os.path.isdir(pages_folder_path):
            for file_name in os.listdir(pages_folder_path):
                if file_name.endswith('.json') and is_valid_json(os.path.join(pages_folder_path, file_name)):
                    json_file_path = os.path.join(pages_folder_path, file_name)
                    with open(json_file_path, 'r', encoding='utf-8') as json_file:
                        data = json.load(json_file)
                        html_content = data.get('html_content', '')

                        if html_content:
                            title_tag, meta_tags = extract_tags_from_html(html_content)
                            print(f"Title: {title_tag}")
                            print(f"Meta Tags: {meta_tags}")
                            row["Title tag"] = title_tag
                            row["Meta tags"] = meta_tags
                        else:
                            print(f"No HTML content found in: {json_file_path}")
                    break  # Exit after processing the first JSON file with valid content
        else:
            print(f"'pages' folder not found in: {folder_path}")
    else:
        print(f"Folder not found: {folder_name}")

# Write the updated rows back to the CSV with the corrected fieldnames
with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("CSV file has been updated with Title tag and Meta tags.")

import os
import json
import csv
from bs4 import BeautifulSoup

# Define the path to the data folder
data_folder = 'data'

# Define the CSV file to write to
csv_file = 'data_labeling.csv'

# Function to extract title and meta tags
def extract_html_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract title tag
    title = soup.title if soup.title else "No Title"
    
    # Extract all meta tags
    meta_tags = ', '.join([tag for tag in soup.find_all('meta')])
    
    return title, meta_tags

# Open CSV file for writing
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write header row
    writer.writerow(['Title', 'Meta Tags', 'Category'])
    
    # Loop through each folder (link) in the data folder
    for folder_name in os.listdir(data_folder):
        folder_path = os.path.join(data_folder, folder_name)
        
        if os.path.isdir(folder_path):
            # Look for the 'pages' subfolder
            pages_folder = os.path.join(folder_path, 'pages')
            if os.path.exists(pages_folder) and os.path.isdir(pages_folder):
                # Get the first file in the 'pages' folder (assuming it's JSON with HTML content)
                page_files = os.listdir(pages_folder)
                if page_files:
                    first_file = page_files[0]
                    file_path = os.path.join(pages_folder, first_file)
                    
                    # Read the JSON file
                    with open(file_path, 'r', encoding='utf-8') as f:
                        try:
                            json_content = json.load(f)
                            # Assuming HTML content is stored under 'html_content' key in the JSON file
                            html_content = json_content.get('html_content', '')
                            
                            if html_content:
                                # Extract title and meta tags using BeautifulSoup
                                title, meta_tags = extract_html_content(html_content)
                                
                                # Write to CSV
                                writer.writerow([title, meta_tags, ''])
                            else:
                                print(f"No HTML content found in: {file_path}")
                        
                        except json.JSONDecodeError:
                            print(f"Error reading JSON file: {file_path}")
            else:
                print(f"'pages' folder not found in: {folder_path}")

print(f"Data labeling CSV has been created at {csv_file}")

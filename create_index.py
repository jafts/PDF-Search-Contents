import os
import fitz  # PyMuPDF
import json

#Define the base folder indexing
base_path = r'C:\my_folder'

def create_index(folder_path, index_file):
    # Load existing index if it exists, or create a new one
    if os.path.exists(index_file):
        with open(index_file, 'r') as f:
            index = json.load(f)
    else:
        index = {}

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf") and filename not in index:
            print(f"Indexing {filename}")
            file_path = os.path.join(folder_path, filename)

            try:
                pdf_document = fitz.open(file_path)
            except fitz.EmptyFileError:
                print(f"Skipping empty file: {filename}")
                continue

            text_content = ''
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                text_content += page.get_text("text")

            pdf_document.close()

            if text_content.strip():
                index[filename] = text_content

    # Update the index file
    with open(index_file, 'w') as f:
        json.dump(index, f)

# Loop through each directory in base_path
for folder_name in os.listdir(base_path):
    folder_path = os.path.join(base_path, folder_name)
    if os.path.isdir(folder_path):
        index_file = os.path.join(folder_path, 'index.json')
        create_index(folder_path, index_file)

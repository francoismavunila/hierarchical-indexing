import os
import re
import json
import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt')

def create_hierarchical_index(text):
    # Regex patterns to identify chapters and sections
    chapter_pattern = r'(Chapter \d+|CHAPTER \d+)'
    section_pattern = r'(Section \d+\.\d+|SECTION \d+\.\d+)'

    index = {"root": {"title": "Book", "children": []}}
    current_chapter = None
    current_section = None

    lines = text.split('\n')
    for line in lines:
        line = line.strip()

        # Detect chapters
        if re.match(chapter_pattern, line):
            current_chapter = {"title": line, "children": []}
            index["root"]["children"].append(current_chapter)

        # Detect sections
        elif re.match(section_pattern, line) and current_chapter:
            current_section = {"title": line, "content": ""}
            current_chapter["children"].append(current_section)

        # Add content to sections
        elif current_section:
            current_section["content"] += " " + line

    return index

def save_index(index, output_path):
    with open(output_path, 'w') as file:
        json.dump(index, file, indent=2)

def main():
    data_dir = 'extracted_texts/'
    output_dir = 'indexes/'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for text_file in os.listdir(data_dir):
        if text_file.endswith('.txt'):
            text_path = os.path.join(data_dir, text_file)
            with open(text_path, 'r') as file:
                text = file.read()
                index = create_hierarchical_index(text)
                output_path = os.path.join(output_dir, text_file.replace('.txt', '_index.json'))
                save_index(index, output_path)
                print(f"Created index for {text_file} and saved to {output_path}")

if __name__ == "__main__":
    main()

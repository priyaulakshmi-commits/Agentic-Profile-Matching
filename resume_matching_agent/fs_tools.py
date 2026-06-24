import os

def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

def list_files(directory):
    return os.listdir(directory)

def search_in_file(file_path, keyword):
    content = read_file(file_path)
    return keyword.lower() in content.lower()
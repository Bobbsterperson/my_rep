import os
import sqlite3


def get_directory():
    return os.getcwd()


def list_items(directory):
    files = os.listdir(directory)
    return files


def get_data(directory, files):
    pure_meta = []
    for n in files:
        full_path = os.path.join(directory, n)
        if os.path.isdir(full_path):
            if n == "venv":
                continue
            sub_files = list_items(full_path)
            sub_meta = get_data(full_path, sub_files)
            pure_meta.extend(sub_meta)
        else:
            file_stat = os.stat(full_path)
            name = os.path.basename(full_path)
            size = file_stat.st_size
            pure_meta.append((name, size, directory))
    return pure_meta


def sorted_data(data):
    return sorted(data, key=lambda x: x[1])


def create_and_write_text_file(data):
    with open('sorted_metadata.txt', 'w') as file:
        for item in data:
            file.write(f"Directory: {item[2]} - Name: {item[0]} - Size: {item[1]} bytes\n")
        file.write("\n")


def create_and_write_to_database(data):
    conn = sqlite3.connect("sqlite.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS file_metadata 
                          (id INTEGER PRIMARY KEY, name TEXT, size INTEGER, directory TEXT)''')
    for item in data:
        name, size, directory = item
        cursor.execute('''INSERT INTO file_metadata (name, size, directory) 
                              VALUES (?, ?, ?)''', (name, size, directory))
    conn.commit()
    cursor.close()
    conn.close()
    
    
def main():
    directory = get_directory()
    files = list_items(directory)
    data = get_data(directory, files)
    sorted_data_result = sorted_data(data)
    create_and_write_text_file(sorted_data_result)
    create_and_write_to_database(sorted_data_result)


if __name__ == "__main__":
    main()

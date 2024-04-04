import os
import sqlite3
import argparse


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

def create_and_write_text_file(data, filename='sorted_metadata.txt'):
    with open(filename, 'w') as file:
        for item in data:
            file.write(f"Directory: {item[2]} - Name: {item[0]} - Size: {item[1]} bytes\n")
        file.write("\n")


def create_database(cursor, conn):
    cursor.execute('''CREATE TABLE IF NOT EXISTS file_metadata 
                    (id INTEGER PRIMARY KEY, name TEXT, size INTEGER, directory TEXT)''')
    conn.commit()

def write_to_database(data, cursor, conn):
    for item in data:
        name, size, directory = item
        cursor.execute('''INSERT INTO file_metadata (name, size, directory) 
                        VALUES (?, ?, ?)''', (name, size, directory))
    conn.commit()
    
def get_data_from_database(cursor):
    cursor.execute("SELECT * FROM file_metadata")
    return cursor.fetchall()

def save_in_database(data):
    with sqlite3.connect("sqlite.db") as conn:
        cursor = conn.cursor()
        create_database(cursor, conn)
        write_to_database(data, cursor, conn)
        conn.commit()
        cursor.close()
        

def parse_arguments():
    parser = argparse.ArgumentParser(description="Output file metadata to either a text file or a SQLite database.")
    parser.add_argument("-t", "--text", action="store_true", help="Output to text")
    parser.add_argument("-db", "--database", action="store_true", help="Output to SQLite database")
    args = parser.parse_args()

    if args.text:
        return 'text'
    elif args.database:
        return 'database'
    else:
        parser.error("Please specify either '-t' for text file or '-db' for SQLite database.")


def main():
    output_type = parse_arguments()
    directory = (os.getcwd())
    files = os.listdir(directory)
    data = get_data(directory, files)
    sorted_data_result = sorted(data, key=lambda x: x[1])
    
    if output_type == 'text':
        create_and_write_text_file(sorted_data_result)
    elif output_type == 'database':
        save_in_database(sorted_data_result)
    else:
        print("Invalid output type specified. Please specify either '-t' for text file or '-db' for SQLite database.")


if __name__ == "__main__":
    main()
    
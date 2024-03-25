import os


def find_dir():
    current_directory = os.getcwd()
    return current_directory


def list_items():
    current_directory = find_dir()
    directory = os.path.expanduser(current_directory)
    files = os.listdir(directory)

    return files


def get_data():
    pure_meta = []

    for n in list_items():
        name = os.path.basename(n)
        size = os.path.getsize(n)
        pure_meta.append((name, size))

    return pure_meta


def sorted_data():
    return sorted(get_data(), key=lambda x: x[1])


def text_file():
    with open('sorted_metadata.txt', 'w') as file:
        for item in sorted_data():
            file.write(f"Name: {item[0]} - Size: {item[1]} bytes\n")


text_file()
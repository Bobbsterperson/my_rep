import os


def get_directory():
    return os.getcwd()


def list_items():
    current_directory = get_directory()
    directory = os.path.expanduser(current_directory)
    files = os.listdir(directory)

    return files


def get_data():
    pure_meta = []

    for n in list_items():
        full_path = os.path.join(get_directory(), n)
        file_stat = os.stat(full_path)
        name = os.path.basename(full_path)
        size = file_stat.st_size
        pure_meta.append((name, size))

    return pure_meta


def sorted_data():
    return sorted(get_data(), key=lambda x: x[1])


def create_text_file():
    return open('sorted_metadata.txt', 'w')


def write_to_file(file):
    for item in sorted_data():
        file.write(f"Name: {item[0]} - Size: {item[1]} bytes\n")


def text_file():
    file = create_text_file()
    write_to_file(file)


def main():
    text_file()


if __name__ == "__main__":
    main()
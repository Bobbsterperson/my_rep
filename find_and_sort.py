import os


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
            pure_meta.append((name, size))
    return pure_meta


def sorted_data(data):
    return sorted(data, key=lambda x: x[1])


def create_and_write_text_file(data):
    with open('sorted_metadata.txt', 'w') as file:
        for item in data:
            file.write(f"Name: {item[0]} - Size: {item[1]} bytes\n")
        file.write("\n")


def main():
    directory = get_directory()
    files = list_items(directory)
    data = get_data(directory, files)
    sorted_data_result = sorted_data(data)
    create_and_write_text_file(sorted_data_result)


if __name__ == "__main__":
    main()

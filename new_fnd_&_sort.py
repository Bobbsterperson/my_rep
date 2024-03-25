import os


def list_items():
    current_directory = os.getcwd()
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


def sort(name, size):
    return sorted(name, key=lambda x: x[size])


metadata = get_data()
sorted_data = sort(metadata, 1)


for i in sorted_data:
    with open('sorted_metadata.txt', 'w') as file:
        for item in sorted_data:
            file.write(f"{item[0]} - Size: {item[1]} bytes\n")
import os
import sorted_file

file_names = []
file_size = []

directory = os.path.expanduser("~/Desktop/music")
files = os.listdir(directory)

for file_name in files:
    file_names.append(file_name)

# print(f"{file_names} \n")
# meta_data = os.stat(file_names[0])

file_paths = []

for i in file_names:
    file_paths.append(f"~/Desktop/music/{i}")

# print(file_paths)

pure_meta = []

for d in file_paths:
    meta_data = os.path.expanduser(d)
    data = os.stat(meta_data)
    # print(data)
    pure_meta.append(data)

for sz in pure_meta:
    file_size.append(sz.st_size)

couple = list(zip(file_size, file_names))

sp = sorted(couple)
sorted_file.add_by_order(sp)

print(f"{sorted_file.sorted_files}\n")


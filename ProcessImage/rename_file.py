import os


def rename_file(file_name):
    splited = file_name.split("_")
    return str(splited[0].zfill(5)) + "_" + "_".join(splited[1:])

path = "..\\images"

for dir in os.listdir(path):
    dir_path = os.path.join(path, dir)
    for file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file)
        os.rename(file_path, os.path.join(dir_path, rename_file(file)))
        print(os.path.join(dir_path, rename_file(file)))
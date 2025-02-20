import os, shutil

def copy_fun(path: str, destination_dir: str):
    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)
    os.mkdir(destination_dir)
    for file in os.listdir(path):
        new_path = os.path.join(path, file)
        if os.path.isfile(new_path):
            print(f"Copy file: {new_path} to destination {destination_dir}")
            shutil.copy(new_path, os.path.join(destination_dir, file))
        else:
            new_destination = os.path.join(destination_dir, file)
            print(f"Crating new directory: {new_destination}")
            os.mkdir(new_destination)
            copy_fun(new_path, new_destination)
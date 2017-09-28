import os


def mkdir(dir):
    if (os.path.exists(dir) == False):
        os.mkdir(dir)

def push_data_to_stack(stack, file_path, file_name):
    sub_folder = os.listdir(file_path)
    for element in sub_folder:
        element = file_name + '/' + element
        stack.append(element)
import os
import sys


def split(file_path, prefix):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    lines.append('\n')

    num = 1
    buffer = list()
    for line in lines:
        if line is '\n':
            if len(buffer) > 0 and buffer[0].startswith('; Static profile'):
                with open(f'{prefix}.{num}.opt', 'w') as file:
                    file.writelines(buffer)
                    num += 1
            buffer = list()
        else:
            buffer.append(line)


def main():
    try:
        file_path = sys.argv[1]
        dir_name = os.path.dirname(file_path)
        base_name = os.path.basename(file_path)
        file_name, file_ext = os.path.splitext(base_name)
        prefix = dir_name + os.path.sep + file_name
        split(file_path, prefix)
    except Exception as e:
        print(e)


main()
import os
import argparse
import shutil
import winreg

def create_file(fname) -> None:
    try:
        f = open(fname, "x")
        f.close()
    except:
        print("Error with creation")


def delete_file(fname) -> None:
    try:
        os.remove(fname)
    except:
        print("No such file")

def write_file(fname, text):
    try:
        f = open(fname, "w")
        f.write(text)
        f.close()
    except:
        print("Error")

def read_file(fname):
    try:
        f = open(fname, "r")
        print("File contents:")
        print(f.read())
        f.close()
    except:
        print("Error")

def copy_file(source, destination):
    try:
        shutil.copyfile(source, destination)
    except:
        print("Error with copying")

def rename_file(fname, new_name):
    try:
        os.rename(fname, new_name)
    except:
        print("No such file")

def main():
    parser = argparse.ArgumentParser(description='FS/Registry management')
    parser.add_argument('--create', type=str, help='Creating a file')
    parser.add_argument('--delete', type=str, help='Deleting a file')
    parser.add_argument('--write', nargs=2, type=str, help='Writing to a file')
    parser.add_argument('--read', type=str, help='Reading from a file')
    parser.add_argument('--rename', nargs=2, type=str, help='Renaming a file')
    parser.add_argument('--copy', nargs=2, type=str, help='Copying a file from one directory to another')
    args = parser.parse_args()

    if (args.create): create_file(args.create)
    elif (args.delete): delete_file(args.delete)
    elif (args.write): write_file(args.write[0], args.write[1])
    elif (args.read): read_file(args.read)
    elif (args.rename): rename_file(args.rename[0], args.rename[1])
    elif (args.copy): copy_file(args.copy[0], args.copy[1])
    else: print("Something's gone wrong")

if __name__ == "__main__":
    main()

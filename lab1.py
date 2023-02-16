import os
import argparse
import shutil
import winreg


def create_file(fname: str) -> None:
    try:
        with open(fname, "x") as fd:
            pass
    except FileExistsError:
        print("File already exists")


def delete_file(fname: str) -> None:
    try:
        os.remove(fname)
    except FileNotFoundError:
        print("No such file")


def write_file(fname: str, text: str) -> None:
    try:
        with open(fname, "w") as fd:
            fd.write(text)
    except FileNotFoundError:
        print("Error")
    except PermissionError:
        print("Permission denied")


def read_file(fname: str) -> None:
    try:
        with open(fname, "r") as fd:
            print("File contents:")
            print(fd.read())
    except FileNotFoundError:
        print("No such file")


def copy_file(source: str, destination: str) -> None:
    try:
        shutil.copyfile(source, destination)
    except FileNotFoundError:
        print("No such file")


def rename_file(fname: str, new_name: str) -> None:
    try:
        os.rename(fname, new_name)
    except FileNotFoundError:
        print("No such file")


def create_key(key: str) -> None:
    try:
        path = 'Software\\'
        path += key
        reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        winreg.CreateKey(reg, path)
    except PermissionError:
        print("Permission denied")


def delete_key(key: str) -> None:
    try:
        path = 'Software\\'
        path += key
        reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        winreg.DeleteKey(reg, path)
    except PermissionError:
        print("Permission denied")


def value_key(key: str, name: str, value: str) -> None:
    try:
        path = 'Software\\'
        path += key
        reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        open_key = winreg.OpenKeyEx(reg, path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(open_key, name, 0, winreg.REG_SZ, value)
        winreg.CloseKey(reg)
    except PermissionError:
        print("Permission denied")


def main():
    ## FILE SYSTEM ##
    parser = argparse.ArgumentParser(description='FS/Registry management')
    parser.add_argument('-cr', '--create', type=str, help='Creating a file')
    parser.add_argument('-d', '--delete', type=str, help='Deleting a file')
    parser.add_argument('-w', '--write', nargs=2,
                        type=str, help='Writing to a file')
    parser.add_argument('-r', '--read', type=str, help='Reading from a file')
    parser.add_argument('-rn', '--rename', nargs=2,
                        type=str, help='Renaming a file')
    parser.add_argument('-c', '--copy', nargs=2, type=str,
                        help='Copying a file from one directory to another')

    ## REGISTRY ##
    parser.add_argument('-kc', '--kcreate', type=str, help='Creating a key')
    parser.add_argument('-kd', '--kdelete', type=str, help='Deleting a key')
    parser.add_argument('-kv', '--kvalue', nargs=3, type=str,
                        help='Writing a value to a keyy')

    args = parser.parse_args()

    if (args.create):
        create_file(args.create)
    elif (args.delete):
        delete_file(args.delete)
    elif (args.write):
        write_file(args.write[0], args.write[1])
    elif (args.read):
        read_file(args.read)
    elif (args.rename):
        rename_file(args.rename[0], args.rename[1])
    elif (args.copy):
        copy_file(args.copy[0], args.copy[1])
    elif (args.kcreate):
        create_key(args.kcreate)
    elif (args.kdelete):
        delete_key(args.kdelete)
    elif (args.kvalue):
        value_key(args.kvalue[0], args.kvalue[1], args.kvalue[2])
    else:
        print("Something's gone wrong")


if __name__ == "__main__":
    main()

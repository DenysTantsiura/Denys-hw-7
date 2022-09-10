"""
A simple junk sorter program.
Many people have a folder on their desktop called something like "unsorted junk"...
This program sorts by certain categories (look in c_exten.py) everything known in the specified folder, and even unpacks archives and deletes empty directories
Run example:
>>> python clean.py /user/Desktop/Мотлох/Junk
"""

import sys
import pathlib
import shutil
from clean_folder import *


# ?: 'pathlib.Path'  OR : 'pathlib.WindowsPath or pathlib.PosixPath' ?
def test_extensions(var_exts: str, current_fs_obj: pathlib.Path):
    '''
    to check file extension and filling file listings
    incoming: the extension - string, the current file object - Path
    out (return): None
    '''
    global unknown_extensions  # ??? in other program works fine without "global"
    global known_extensions  # ??? in other program works fine without "global"
    flag_ok = 0  # known extension?
    var_exts = var_exts.lower()
    for category, ext_list in data_base_of_extensions.items():
        for it_ext in ext_list:  # run for all known extensions
            if it_ext == var_exts:  # known extension
                known_extensions.append(var_exts)
                unknown_extensions = list(set(unknown_extensions))
                # eval is dangerous! Try...:
                eval(category).append(current_fs_obj)
                # getattr(sys.modules[__name__], category).append(current_fs_obj)
                flag_ok = 1
    if flag_ok == 0:  # no known extension = unknown extension
        unknown_extensions.append(var_exts)
        unknown_extensions = list(set(unknown_extensions))


def junk_scanner(dir_in: pathlib.Path):
    """
    run recursive listing of directories to check file extension and filling file listings to sort and normalize
    incoming: the folder - Path
    out (return): None
    """
    for fs_obj in dir_in.iterdir():  # all obj in dir
        if fs_obj.is_dir():  # if dirr
            if fs_obj.name not in main_directories:
                # all_subdirectories.append(fs_obj)  # no normalized dir to list?
                junk_scanner(fs_obj)
        if fs_obj.is_file():
            if (fs_obj.suffix)[1:]:  # extension
                # str(extension), pathlib.Path(file_obj) to:
                test_extensions((fs_obj.suffix)[1:], fs_obj)


def new_name(try_new_name: str, add_cx: int):
    """
    rechange number(add_cx) in filename(try_new_name)
    incoming: try_new_name - string, add_cx - int
    out (return): new name - string
    """
    return (".".join(try_new_name.split(".")[:-1]))[:-len(str(add_cx-1))] + str(
        add_cx) + '.' + try_new_name.split(".")[len(try_new_name.split("."))-1]


def check_new_names(dir_in: pathlib.Path, norm_name_obj: pathlib.Path):
    '''checks for the existence of a file in a folder after normalized, 
    and return str(free new_name)
    incoming: dir_in - Path, norm_name_obj - Path
    out (return): new name - string
    '''
    if norm_name_obj.is_dir() or not norm_name_obj.suffix:
        norm_name = norm_name_obj.name  # name.ext or name
        norm_name = normalize(norm_name)  # str dir
        obj_candidate = dir_in.joinpath(norm_name)
    # elif norm_name_obj.is_file() and norm_name_obj.suffix:
    else:
        norm_name = norm_name_obj.name[:-len(norm_name_obj.suffix)]
        norm_name = normalize(norm_name)  # str file w/o ext
        obj_candidate = dir_in.joinpath(
            "".join([norm_name, norm_name_obj.suffix]))
    new_counter = 0
    while True:  # Is it better to use recursion? not now
        if obj_candidate.exists():  # norm_fs_obj.is_file() or norm_fs_obj.is_dir()/// symb link?
            new_counter += 1  # new number for new name
            # rechange number in filename, new name with number:
            norm_name = new_name(norm_name, new_counter)
            if norm_name_obj.is_file() and norm_name_obj.suffix:
                obj_candidate = dir_in.joinpath(
                    "".join([norm_name, norm_name_obj.suffix]))
            else:  # dir or len(norm_name_obj.suffix) == 0
                # if exist dots in name of directory (false suffix)
                obj_candidate = dir_in.joinpath(norm_name)
        else:
            break
    if norm_name_obj.is_file() and norm_name_obj.suffix:
        return "".join([norm_name, norm_name_obj.suffix])
    else:
        return norm_name


def freeing_the_reserved_name_for_the_sorting_directory(main_directory: pathlib.Path):
    '''freeing (rename existing) the reserved name for the sorting directory if the name already exists
    incoming: main_directory - Path
    out (return): None
    '''
    for item_category in data_base_of_extensions:  # sort all categories
        new_counter = 0
        need_free_name = main_directory.joinpath(item_category)
        if need_free_name.is_file():  # the existing file
            # looking for a new name for the file
            obj_candidate = pathlib.Path(str(need_free_name)+str(new_counter))
            while True:  # Is it better to use recursion? not now
                if obj_candidate.exists():  # norm_fs_obj.is_file() or norm_fs_obj.is_dir()/// symb link?
                    new_counter += 1  # new number for new name
                    # rechange number in dir-name, new name with adding number:
                    norm_name = new_name(obj_candidate.name, new_counter)
                    obj_candidate = main_directory.joinpath(norm_name)
                else:
                    break
            need_free_name.replace(obj_candidate)
    # return True


def simple_sorterer(file_to_sort: pathlib.Path, main_directory: pathlib.Path, simple_category: str):
    '''simple sorterer 
    incoming: file_to_sort - Path, main_directory - Path, simple_category - str
    out (return): None (replacing to new free name)
    '''
    target_dir = main_directory.joinpath(simple_category)
    # ADD! rename file with "simple_category" name, if exist = def freeing_the_reserved_name_for_the_sorting_directory
    target_dir.mkdir(exist_ok=True)
    # if name for file is non-free? check_new_names...
    # for check and normalize..., # pathlib.Path, pathlib.Path to:
    free_name = check_new_names(target_dir, file_to_sort)
    file_to_sort.replace(target_dir.joinpath(free_name))


def archives_sorterer(current_arch: pathlib.Path, main_directory: pathlib.Path):
    """
    Unpack and then delete each archive or report the wrong archive
    incoming: current_arch - Path, main_directory - Path
    out (return): False OR Unpack and then delete the archive
    """
    target_dir = main_directory.joinpath("archives")
    # ADD! rename file with "archives" name, if exist = def freeing_the_reserved_name_for_the_sorting_directory
    target_dir.mkdir(exist_ok=True)
    arch_dir = check_new_names(
        target_dir, (current_arch.parent).joinpath(current_arch.name[:-len(current_arch.suffix)]))
    arch_dir = target_dir.joinpath(arch_dir)
    arch_dir.mkdir(exist_ok=True)
    try:
        shutil.unpack_archive(str(current_arch.absolute()),
                              str(arch_dir.absolute()))
    except:
        print('Error while unpacking archive. Wrong archive?')
        arch_dir.rmdir()
        return False
    # when remove archive? now if unpacking is successful:
    current_arch.unlink()
    # return True


def fun_print_author():  # for simple testing home-task module 7
    print("Created: Denys TANTSIURA\n")


def delete_empty_dir(dir_in: pathlib.Path):  # pathlib.Path
    """
    run recursive listing of directories to remove empty-dir or normalize, if else
    incoming: dir_in - Path
    out (return): None (try to delete the folder - Removal if it's empty and normalize name if else
    """
    for fs_obj in dir_in.iterdir():  # all obj in dir
        if fs_obj.is_dir():  # if dirr
            if fs_obj.name not in main_directories:  # such incorrect initial conditions in the task
                delete_empty_dir(fs_obj)
                try:
                    fs_obj.rmdir()  # if empty - silent removal
                except:  # ... else if... what Error? and else?
                    # chek and normalize # pathlib.Path, pathlib.Path -> str: new_name_dir
                    new_name_dir = check_new_names(dir_in, fs_obj)
                    fs_obj.replace(dir_in.joinpath(new_name_dir))


def start_cleaner(target_directory: str):  # user input at start
    """
    main function 
    (all files and folders are normalized...
     but 
     Files whose extensions are unknown remain unchanged!)
    incoming: target_directory - Path
    out (return): None (many functions)
    """
    print('OK, let`s do it')
    directory = pathlib.Path(target_directory)
    if not directory.is_dir():
        print('Sorry, but "target directory" does not exist ',
              target_directory, "\n", directory.is_dir())
        exit()
    # run recursive listing of directories to check file extension and populate file listings to sort and normalize
    junk_scanner(directory)  # pathlib.Path

    freeing_the_reserved_name_for_the_sorting_directory(directory)

    for item_category in data_base_of_extensions.keys():  # sort all normal category without archives
        if item_category != "archives":
            # eval is dangerous! Try...: getattr(sys.modules[__name__], item_category)
            for fs_obj in eval(item_category):  # in each list
                # pathlib.Path, pathlib.Path, str("images/... etc") to:
                simple_sorterer(fs_obj, directory, item_category)

    for fs_obj in archives:  # unpack archives
        # pathlib.Path, pathlib.Path
        archives_sorterer(fs_obj, directory)
        # normalize files from the archive???

    # deleting empty directories or normalize
    delete_empty_dir(directory)  # pathlib.Path


def main():
    """
    The main function checks the startup parameters and the presence of a folder and starts the sorting process ...
    """
    if len(sys.argv) < 2:
        print('The path of the folder to be cleaned is not specified')
        exit()
    path = sys.argv[1]
    if not pathlib.Path(path).is_dir():  # pathlib.Path(path).exists()
        print(
            f'Path incorrect, no target directory specified. Checking "{path}"')
        exit()
    start_cleaner(path)  # start_cleaner("D:\\tests")


if __name__ == "__main__":
    # Show that after MAIN function the code will be completed and nothing is needed after it
    exit(main())

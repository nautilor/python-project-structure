#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
from os import mkdir
from os.path import join, isfile, exists
import base64
from typing import List
from dataclasses import dataclass, field
from os import name as os_name


@dataclass
class SubModule:
    """ the representation of a module """

    name: str


@dataclass
class Module:
    """ the representation of a submodule """

    name: str
    sub_modules: List[SubModule] = field(default_factory=list)


# No colors on Windows as it does not supports ANSI (⌒_⌒;)
if os_name != "nt":
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
else:
    HEADER = ""
    OKBLUE = ""
    OKCYAN = ""
    OKGREEN = ""
    WARNING = ""
    FAIL = ""
    ENDC = ""
    BOLD = ""
    UNDERLINE = ""


# the root base folder name
BASE_ROOT_DIR = "root"
# the __init__.py file name used inside the root, modules and submodules
BASE_INIT_FILE = "__init__.py"
# the starting point of the program
BASE_MAIN_FILE = "__main__.py"
# the __main__.py content in a base64 encoded string
BASE_MAIN_CONTENT = (
    "IyEvdXNyL2Jpbi9lbnYgcHl0aG9uM1xuXG5kZWYgbWFpbigpOlxuICAgIHBhc3N"
    "cblxuaWYgX19uYW1lX18gPT0gIl9fbWFpbl9fIjpcbiAgICBtYWluKCk="
)
# modules to create
BASE_MODULES = [
    Module("model"),
    Module("util"),
    Module("constant"),
    Module("helper", [SubModule("telegram"), SubModule("telegram")]),
]


def define_arguments() -> Namespace:
    """create all arguments for the project and parse the data

    Returns:
        Namespace: the parsed arguments
    """
    args: ArgumentParser = ArgumentParser()
    args.add_argument("-p", "--project", required=True, metavar="<name>")
    return args.parse_args()


def mkbase(project: str):
    """create the base structure including the project folder along with the __main__.py file

    Args:
        project (str): the project name
    """
    print(f"{OKBLUE}I: {OKGREEN}Creating project {project}")
    mkdir(project)
    mkmain(project)


def mkfile(name: str):
    """function to create an empty file given it's path

    Args:
        name (str): the filename to create
    """
    open(name, "a").close()


def mkroot(project: str) -> str:
    """create the root folder inside the program with the __init__.py file

    Args:
        project (str): the project name

    Returns:
        str: the path of the root folder
    """
    print(f"{OKBLUE}I: {OKGREEN}Creating root directory for modules")
    root: str = join(project, BASE_ROOT_DIR)
    mkdir(root)
    mkfile(join(root, BASE_INIT_FILE))
    return root


def mkmain(project: str):
    """create the __main__.py file for a

    Args:
        project (str): the project name
    """
    print(f"{OKBLUE}I: {OKGREEN}Creating __main__.py file with content")
    with open(join(project, BASE_MAIN_FILE), "w") as mfile:
        content: bytes = base64.decodestring(BASE_MAIN_CONTENT.encode("UTF-8"))
        mfile.write(content.decode("UTF-8").replace("\\n", "\n"))


def mkmodule(module: Module, root: str):
    """create a module structure inside the root folder along with all the submodules

    Args:
        module (Module): The module to create
        root (str): the path of the root folder for the project
    """
    name = join(root, module.name)
    if mkexists(name):
        print(f"{WARNING}W: {UNDERLINE}Ignoring duplicated module {module.name}{ENDC}")
        return
    print(f"{OKBLUE}I: {OKGREEN}Creating module {module.name}")
    mkdir(name)
    mkfile(join(name, BASE_INIT_FILE))
    for sub_module in module.sub_modules:
        sname = join(name, sub_module.name)
        if mkexists(sname):
            print(f"{WARNING}W: {UNDERLINE}Ignoring sub_module {sub_module.name}{ENDC}")
            continue
        print(f"{OKBLUE}I: {OKGREEN}Creating sub_module {sub_module.name}")
        mkdir(sname)
        mkfile(join(sname, BASE_INIT_FILE))


def mkproject(name: str):
    """create the project structure

    Args:
        name (str): the project name
    """
    if mkexists(name):
        print(f"{FAIL}{BOLD}E: {UNDERLINE}A file with the same name is already present")
    else:
        mkbase(name)
        root: str = mkroot(name)
        [mkmodule(module, root) for module in BASE_MODULES]
        print(
            f"{OKBLUE}I: {OKGREEN}Your project has been created, you can start coding"
        )


def mkexists(name: str) -> bool:
    """check if a project or file with the same name exists

    Args:
        name (str): the project name

    Returns:
        bool: wheter it exists or not
    """
    return isfile(name) or exists(name)


def main():
    """ main program """
    print(ENDC)
    args: Namespace = define_arguments()
    mkproject(args.project)
    print(ENDC)


if __name__ == "__main__":
    main()
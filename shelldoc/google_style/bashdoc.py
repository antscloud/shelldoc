import re
from collections import defaultdict
import os
import argparse

SHEBANG = re.compile(r"^#!.*")
FUNCTION = re.compile(r"^\s*function\s*(\w+)\s*\(\w*\)\s*\{")
BIG_COMMENT = re.compile(r"^##.*")
SMALL_COMMENT = re.compile(r"^#.*")
GLOBALS = re.compile(r"^#\s*[Gg]lobal\s*:?")
ARGUMENTS = re.compile(r"^#\s*[Aa]rguments?\s*:?")
OUTPUTS = re.compile(r"^#\s*[Oo]utputs?\s*:?")
RETURNS = re.compile(r"^#\s*[Rr]eturns?\s*:?")
TODO = re.compile(r"^#\s*TODO(\(\w*\))?\s*:?\s*(.*)")
INDENT = re.compile(r"^#\s+(.*)\n")
EMPTY_LINE = re.compile(r"^\s*$")
START_WITH_SHARP = re.compile(r"^#+(.*)")

###############################################################################
# EXTRACT DOCUMENTATION
###############################################################################


def get_file_documentation(lines):
    file_documentation = ""
    for no, line in enumerate(lines):
        is_empty_line = EMPTY_LINE.match(line)
        sharped_line = START_WITH_SHARP.match(line)
        is_shebang = SHEBANG.match(line)
        is_doc = sharped_line and not is_shebang
        if is_doc:
            file_documentation += sharped_line.group(1)
        if is_empty_line and not is_doc:
            break
    return file_documentation


def get_boudaries_of_function_doc(lines, no_fun):
    begin_description, end_description = None, None
    while no_fun != 0:
        no_fun -= 1
        line = lines[no_fun]
        if end_description is None:
            if BIG_COMMENT.match(line) or SMALL_COMMENT.match(line):
                end_description = no_fun
            else:
                break
        elif begin_description is None:
            if BIG_COMMENT.match(line):
                begin_description = no_fun
            elif SMALL_COMMENT.match(line):
                continue
            else:
                break
    return begin_description, end_description


def is_important_keyword(line):
    if GLOBALS.match(line):
        return True
    if ARGUMENTS.match(line):
        return True
    if OUTPUTS.match(line):
        return True
    if RETURNS.match(line):
        return True
    return False


def get_function_args(no_line, lines):
    args = []
    no_line += 1
    line = lines[no_line]
    while not is_important_keyword(line):
        if FUNCTION.match(line):
            break

        arg_of_keyword = INDENT.match(line)
        if arg_of_keyword:
            args.append(arg_of_keyword.group(1))
        no_line += 1
        line = lines[no_line]
    return args


def get_function_documentation(lines, no):
    fun_doc = {
        "description": "",
        "globals": [],
        "arguments": [],
        "returns": [],
        "outputs": [],
    }

    begin_description, end_description = get_boudaries_of_function_doc(lines, no)

    if begin_description is None or end_description is None:
        return fun_doc

    description_finished = False
    for no_line in range(begin_description + 1, end_description):
        line = lines[no_line]
        if GLOBALS.match(line):
            fun_doc["globals"] = get_function_args(no_line, lines)
        elif ARGUMENTS.match(line):
            fun_doc["arguments"] = get_function_args(no_line, lines)
        elif RETURNS.match(line):
            fun_doc["returns"] = get_function_args(no_line, lines)
        elif OUTPUTS.match(line):
            fun_doc["outputs"] = get_function_args(no_line, lines)
        if not description_finished:
            if is_important_keyword(line):
                description_finished = True
            elif BIG_COMMENT.match(line):
                description_finished = True
            else:
                fun_doc["description"] += INDENT.match(line).group(1)
    return fun_doc


def get_todo_documentation(line):
    return TODO.match(line).group(2)


def get_shebang(line):
    return line.strip()


def get_documentation(file, dest):
    documentation = defaultdict(dict)
    documentation["description"] = ""
    with open(file, "r") as f:
        shebang_find = False
        lines = f.readlines()
        documentation["description"] = get_file_documentation(lines)
        for no, line in enumerate(lines):
            if SHEBANG.match(line) and not shebang_find:
                documentation["shebang"] = get_shebang(line)
                shebang_find = True
                continue
            if FUNCTION.match(line):
                function = FUNCTION.match(line).group(1)
                documentation["functions"][function] = get_function_documentation(
                    lines, no
                )
                continue
            if TODO.match(line):
                if "todos" not in documentation:
                    documentation["todos"] = []
                documentation["todos"].append(get_todo_documentation(line))
                continue
    return documentation


###############################################################################
# WRITE DOCUMENTATION
###############################################################################


def write_todos(documentation, f):
    if "todos" in documentation:
        f.write("## Todos\n")
        for todo in documentation["todos"]:
            f.write(f"- [ ] {todo}\n")


def write_functions(documentation, f):
    for key in documentation["functions"]:
        f.write(f"## `{key}()`\n")
        if len(documentation["functions"][key]["description"]) != 0:
            description = documentation["functions"][key]["description"]
            f.write(f"**Description**\n")
            f.write(f"{description}\n")
            f.write("\n")

        if len(documentation["functions"][key]["arguments"]) != 0:
            f.write(f"**Arguments**\n")
            for line in documentation["functions"][key]["arguments"]:
                f.write(f"- {line}\n")
                f.write("\n")

        if len(documentation["functions"][key]["returns"]) != 0:
            f.write(f"**Returns**\n")
            for line in documentation["functions"][key]["returns"]:
                f.write(f"- {line}\n")
                f.write("\n")

        if len(documentation["functions"][key]["outputs"]) != 0:
            f.write(f"**Outputs**\n")
            for line in documentation["functions"][key]["outputs"]:
                f.write(f"- {line}\n")
                f.write("\n")


def write_general_description(documentation, f):
    if len(documentation["description"]) != 0:
        f.write(f"## Description\n")
        f.write(f"{documentation['description']}\n")
        f.write("\n")


def write_documentation(files, dest):
    print(f"Write files in {os.path.basename(dest)} folder")
    for file in files:
        documentation = get_documentation(file, dest)
        export_file = os.path.splitext(file)[0] + ".md"
        with open(export_file, "w") as f:
            write_general_description(documentation, f)
            write_functions(documentation, f)
            write_todos(documentation, f)
        print(f"Documentation of {os.path.basename(file)} written.")


def get_parser():
    parser = argparse.ArgumentParser(
        description="Generate documentation from shell script"
    )
    parser.add_argument(
        "-f",
        "--files",
        nargs="+",
        help="Files to generate documentation from",
        required=True,
    )
    parser.add_argument(
        "-d", "--dest", help="Directory to generate documentation in", required=True
    )
    return parser


def test_existence_of_files(files):
    for file in files:
        if not os.path.isfile(file):
            raise FileNotFoundError(f"File {file} does not exist")


def create_destination_if_not_existing(destination):
    if not os.path.isdir(destination):
        os.mkdir(destination)


def main():
    parser = get_parser()
    args = parser.parse_args()
    files = [os.path.abspath(file) for file in args.files]
    dest = os.path.abspath(args.dest)

    test_existence_of_files(files)
    create_destination_if_not_existing(dest)

    write_documentation(files, dest)


if __name__ == "__main__":
    main()

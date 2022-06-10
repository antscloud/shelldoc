import argparse
import os
from shelldoc.google_style.parser import Parser
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def get_parser():
    parser = argparse.ArgumentParser(description="Generate documentation from shell script")
    parser.add_argument(
        "-f", "--files", nargs="+", help="Files to generate documentation from", required=True,
    )
    parser.add_argument(
        "-d",
        "--dest",
        help="Directory to generate documentation in. ./docs by default",
        default="./docs",
    )
    return parser


def test_existence_of_files(files):
    for file in files:
        if not os.path.isfile(file):
            raise FileNotFoundError(f"File {file} does not exist")


def create_destination_if_not_existing(destination):
    if not os.path.isdir(destination):
        os.mkdir(destination)


def write_todos(ast, f):
    if "todos" in ast and ast["todos"]:
        f.write("## Todos\n")
        for todo in ast["todos"]:
            f.write(f"- [ ] {todo}\n")


def _write_function_ref(ast, f, link):
    find = False
    for key in ast["blocks"]:
        if key["function"] == link:
            f.write(f"- [{link}](#{link.lower()})\n")
            find = True
            break
    if not find:
        f.write(f"- [{link}]({link.lower()})\n")


def write_functions(ast, f):
    for key in ast["blocks"]:
        f.write(f"## `{key['function']}()`\n")
        if len(key["description"]) != 0:
            description = key["description"]
            f.write(f"**Description**\n")
            f.write(f"{description}\n")
            f.write("\n")

        for stmt in key["stmts"]:
            for stmt_key in stmt:
                f.write(f"**{stmt_key}**\n")
                for value in stmt[stmt_key]:
                    if len(value) != 0:
                        if stmt_key == "See":
                            _write_function_ref(ast, f, value)
                        else:
                            f.write(f"- {value}\n")
                f.write("\n")


def write_general_description(ast, f):
    if ast["description"]:
        f.write(f"## Description\n")
        f.write(f"{ast['description']}\n")
        f.write("\n")


def write_interpreter(ast, f):
    if "shebang" in ast and ast["shebang"]:
        f.write(f"**Interpreter** : `{ast['shebang'][2:]}`\n")
        f.write("\n")


def write_documentation(files, dest):
    logging.info(f"Write files in {os.path.basename(dest)} folder")
    for file in files:
        with open(file, "r") as f:
            lines = f.readlines()
            ast = Parser(lines).parse()

        export_file = os.path.splitext(os.path.basename(file))[0] + ".md"
        export_file = os.path.join(dest, export_file)
        with open(export_file, "w") as f:
            write_general_description(ast, f)
            write_interpreter(ast, f)
            write_functions(ast, f)
            write_todos(ast, f)
        logging.info(f"Documentation of {os.path.basename(file)} written in {dest}")


def main():
    parser = get_parser()
    args = parser.parse_args()
    files = [os.path.abspath(file) for file in args.files]
    dest = os.path.abspath(args.dest)
    if not os.path.exists(dest):
        os.mkdir(dest)

    write_documentation(files, dest)


if __name__ == "__main__":
    main()

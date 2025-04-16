import os
import sys
import argparse

from IPython import embed

def read_list_file(file_path):
    """
    Read a list file (.il or .wl) and return the list of patterns.
    """
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"List file not found: {file_path}")
        return []


def validate_listfile_content(alist, rootdir):
    results = []
    for file in alist:
        full_path = os.path.join(rootdir, file)

        if os.path.exists(full_path):
            results.append(True)
        else:
            print(f"The file '{file}' does NOT exist.")
            results.append(False)

    # success if all files exist
    return all(results)

def match_pattern(pattern, alist):
    """
    Check if a given path matches any of the line in the alist.
    """
    for line in alist or []:
        if pattern in line:
            return True
    return False

def save_project_structure_and_files(root_path, output_file, ignore_list=None, whitelist=None):
    """
    Save the project structure and contents of all files in the project to a text file,
    considering ignore and whitelist.
    """
    project_structure = []
    files_content = []

    for root, dirs, files in os.walk(root_path):
        # Filter directories and files based on ignore_list and whitelist
        if whitelist:
            dirs[:] = [
                d for d in dirs
                if not match_pattern(d, ignore_list) and
                    match_pattern(d, whitelist)
            ]
        else:
            dirs[:] = [
                d for d in dirs
                if not match_pattern(d, ignore_list)
            ]

        files = [
            f for f in files
            if not match_pattern(f, ignore_list) and
               (not whitelist or match_pattern(f, whitelist))
        ]

        for file in files:
            rel_dir = os.path.relpath(root, root_path)
            rel_file = os.path.join(rel_dir, file)
            project_structure.append(rel_file.replace("\\", "/"))

            try:
                with open(os.path.join(root, file), 'r') as f:
                    content = f.read()
                files_content.append(f"{file}:\n```\n{content}\n```\n")
            except Exception as e:
                files_content.append(f"{file}:\n```\nError reading file: {e}\n```\n")

    with open(output_file, 'w') as f:
        f.write("Project Structure:\n")
        f.write("\n".join(project_structure) + "\n\n")
        f.write("File Contents:\n")
        f.write("\n".join(files_content))


def create_llm_context(rootdir, output_file, files_list):
    """
    Save the project structure and contents of all files in the project to a
    text file
    """
    project_structure = []
    files_content = []

    for file in files_list:
        full_path = os.path.join(rootdir, file)
        project_structure.append(file)

        try:
            with open(full_path, 'r') as f:
                content = f.read()
            files_content.append(f"{file}:\n```\n{content}\n```\n")
        except Exception as e:
            files_content.append(f"{file}:\n```\nError reading file: {e}\n```\n")

    with open(output_file, 'w') as f:
        f.write("Project Structure:\n")
        f.write("\n".join(project_structure) + "\n\n")
        f.write("File Contents:\n")
        f.write("\n".join(files_content))


def main():
    script_dir = os.path.dirname(__file__)
    project_root = os.getcwd()

    parser = argparse.ArgumentParser(description="Save project structure and file contents.")
    parser.add_argument("--il", nargs='?', const=None, default=None,
                        help="Use ignore list file (default: .il)")
    parser.add_argument("--wl", nargs='?', const=None, default=None,
                        help="Use whitelist file (default: .wl)")
    parser.add_argument("--show-locations",
                        help="Show the location of the default .il and .wl files",
                        action="store_true")

    args = parser.parse_args()

    # Determine file paths
    il_file = os.path.join(script_dir, '.il') if not args.il else args.il
    wl_file = os.path.join(script_dir, '.wl') if not args.wl else args.wl

    if args.show_locations:
        print("IL file is located at:", il_file)
        print("WL file is located at:", wl_file)
        sys.exit(0)

    ignore_list = read_list_file(il_file)
    whitelist = read_list_file(wl_file)

    if validate_listfile_content(whitelist, project_root):
        create_llm_context(project_root, 'project_contents.txt', whitelist)
        sys.exit(0)
    else:
        print("N.B.: Original script does not work properly. Exit...")
        sys.exit(1)

    save_project_structure_and_files('.', 'project_contents.txt', ignore_list, whitelist)

import os
import argparse
import configparser
from pathlib import Path
from fnmatch import fnmatch

def load_unify_config(repo_path):
    unify_path = repo_path / '.unify'
    config = {
        "add": [],
        "ignore": [],
        "versioncontrol": "git",  # Default version control
        "outputfile": "unify-output.txt"
    }
    
    if unify_path.exists():
        parser = configparser.ConfigParser(allow_no_value=True)
        parser.read(unify_path)
        
        if 'add' in parser:
            config['add'] = [pattern.strip() for pattern in parser['add'] if pattern.strip()]
        if 'ignore' in parser:
            config['ignore'] = [pattern.strip() for pattern in parser['ignore'] if pattern.strip()]
        if 'versioncontrol' in parser and 'system' in parser['versioncontrol']:
            config['versioncontrol'] = parser['versioncontrol']['system'].strip()
        if 'outputfile' in parser and 'name' in parser['outputfile']:
            config['outputfile'] = parser['outputfile']['name'].strip()
    
    return config

def is_ignored(file_path, ignore_patterns):
    return any(fnmatch(file_path, pattern) for pattern in ignore_patterns)

def is_added(file_path, add_patterns):
    return any(fnmatch(file_path, pattern) for pattern in add_patterns)

def traverse_directory(repo_path, add_patterns, ignore_patterns):
    files = []
    for root, _, filenames in os.walk(repo_path):
        for filename in filenames:
            file_path = os.path.relpath(os.path.join(root, filename), repo_path)
            if is_ignored(file_path, ignore_patterns) and not is_added(file_path, add_patterns):
                continue  # Skip ignored files unless explicitly added
            files.append(file_path)
    return files

def generate_output(repo_path, files, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for file in files:
            file_path = repo_path / file
            with open(file_path, 'r', errors='ignore') as content_file:
                content = content_file.read()
            f.write(f"===============\nFile: {file}\n===============\n{content}\n\n")
    
    with open(output_file, 'r', encoding='utf-8') as f:
        output_content = f.read()
    total_word_count = len(output_content.split())
    total_lines = output_content.count('\n') + 1
    total_files = len(files)
    
    print(f"Total Files: {total_files}")
    print(f"Total Lines: {total_lines}")
    print(f"Total Word Count: {total_word_count}")

def main():
    parser = argparse.ArgumentParser(description="Pack repository into a single AI-friendly file based on .unify config.")
    parser.add_argument('repo_path', type=Path, help="Path to the local repository.")
    args = parser.parse_args()
    
    repo_path = args.repo_path.resolve()
    if not repo_path.is_dir():
        print(f"Error: {repo_path} is not a valid directory.")
        return
    
    config = load_unify_config(repo_path)
    files = traverse_directory(repo_path, config['add'], config['ignore'])
    output_file = repo_path / config['outputfile']
    generate_output(repo_path, files, output_file)
    print(f"Repository packed into {output_file}")

if __name__ == "__main__":
    main()

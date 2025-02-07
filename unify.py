import os
import argparse
from pathlib import Path

def load_gitignore(repo_path):
    gitignore_path = repo_path / '.gitignore'
    if gitignore_path.exists():
        with open(gitignore_path, 'r') as f:
            patterns = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        return patterns
    return []

def is_ignored(file_path, ignore_patterns):
    from fnmatch import fnmatch
    for pattern in ignore_patterns:
        if fnmatch(file_path, pattern):
            return True
    return False

def traverse_directory(repo_path, ignore_patterns):
    files = []
    for root, _, filenames in os.walk(repo_path):
        for filename in filenames:
            file_path = os.path.relpath(os.path.join(root, filename), repo_path)
            if not is_ignored(file_path, ignore_patterns):
                files.append(file_path)
    return files

def generate_output(repo_path, files, output_file, style):
    with open(output_file, 'w') as f:
        if style == 'markdown':
            f.write("# Repository Files\n\n")
        for file in files:
            file_path = repo_path / file
            with open(file_path, 'r', errors='ignore') as content_file:
                content = content_file.read()
            if style == 'markdown':
                f.write(f"## {file}\n\n```\n{content}\n```\n\n")
            else:
                f.write(f"===============\nFile: {file}\n===============\n{content}\n\n")

def main():
    parser = argparse.ArgumentParser(description="Pack repository into a single AI-friendly file.")
    parser.add_argument('repo_path', type=Path, help="Path to the local repository.")
    parser.add_argument('-o', '--output', type=Path, default='repomix-output.txt', help="Output file name.")
    parser.add_argument('--style', choices=['plain', 'markdown'], default='plain', help="Output format style.")
    args = parser.parse_args()

    repo_path = args.repo_path.resolve()
    if not repo_path.is_dir():
        print(f"Error: {repo_path} is not a valid directory.")
        return

    ignore_patterns = load_gitignore(repo_path)
    files = traverse_directory(repo_path, ignore_patterns)
    generate_output(repo_path, files, args.output, args.style)
    print(f"Repository packed into {args.output}")

if __name__ == "__main__":
    main()

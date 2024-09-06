import os
import fnmatch

def read_denied_words(file_path):
    with open(file_path, 'r') as file:
        return [line.strip().lower() for line in file]

def find_denied_words_in_file(file_path, denied_words):
    with open(file_path, 'r') as file:
        content = file.read().lower()
        return [word for word in denied_words if word in content]

def check_files(base_dirs, denied_words):
    report = {}
    for base_dir in base_dirs:
        for root, _, files in os.walk(base_dir):
            for file in files:
                if fnmatch.fnmatch(file, '*.py') or fnmatch.fnmatch(file, '*.yml'):
                    file_path = os.path.join(root, file)
                    found_words = find_denied_words_in_file(file_path, denied_words)
                    if found_words:
                        report[file_path] = found_words
    return report

def main():
    denied_words = read_denied_words('tests/denied_words.txt')
    base_dirs = ['app', 'kubernetes']
    report = check_files(base_dirs, denied_words)

    if report:
        print("Denied words found in the following files:")
        for file_path, words in report.items():
            print(f"{file_path}: {', '.join(words)}")
        exit(1)
    else:
        print("No denied words found.")
        exit(0)

if __name__ == "__main__":
    main()

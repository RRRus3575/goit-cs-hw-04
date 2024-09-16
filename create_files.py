# Функція для створення тестових файлів
def create_test_files():
    files_content = {
        "file1.txt": "This is a sample text file containing keyword1 and keyword2.",
        "file2.txt": "Another file with keyword1 and some additional content.",
        "file3.txt": "This file contains keyword2 and other unrelated content.",
        "file4.txt": "Yet another file without any of the keywords.",
        "file5.txt": "File with multiple keyword1 and keyword2 occurrences. keyword1 keyword2."
    }

    for file_name, content in files_content.items():
        with open(file_name, 'w') as file:
            file.write(content)

    print("Test files created successfully.")

# Виклик функції для створення файлів
create_test_files()

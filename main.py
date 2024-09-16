import multiprocessing
import time
import os

# Функція для пошуку ключових слів у файлі
def search_keywords_in_file(file_path, keywords):
    result = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    if keyword not in result:
                        result[keyword] = []
                    result[keyword].append(file_path)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
    return result

# Функція для обробки файлів у процесах
def process_files_multiprocessing(file_paths, keywords):
    manager = multiprocessing.Manager()
    result_dict = manager.dict()
    jobs = []

    def worker(files):
        local_result = {}
        for file_path in files:
            file_result = search_keywords_in_file(file_path, keywords)
            print(f"Worker processing {file_path}: {file_result}")  
            for keyword, paths in file_result.items():
                if keyword not in local_result:
                    local_result[keyword] = []
                local_result[keyword].extend(paths)
        for keyword, paths in local_result.items():
            if keyword not in result_dict:
                result_dict[keyword] = manager.list() 
            for path in paths:
                if path not in result_dict[keyword]:
                    result_dict[keyword].append(path)

    # Розділення файлів між процесами
    num_processes = 4
    chunk_size = len(file_paths) // num_processes
    for i in range(num_processes):
        start_index = i * chunk_size
        end_index = None if i == num_processes - 1 else (i + 1) * chunk_size
        chunk_files = file_paths[start_index:end_index]
        process = multiprocessing.Process(target=worker, args=(chunk_files,))
        jobs.append(process)
        process.start()

    for job in jobs:
        job.join()

    final_result = {key: list(result_dict[key]) for key in result_dict}
    return final_result

# Приклад використання
if __name__ == "__main__":
    file_paths = ["file1.txt", "file2.txt", "file3.txt", "file4.txt", "file5.txt"]
    keywords = ["keyword1", "keyword2"]

    start_time = time.time()
    results = process_files_multiprocessing(file_paths, keywords)
    end_time = time.time()

    print(f"Multiprocessing Results: {results}")
    print(f"Time Taken: {end_time - start_time:.2f} seconds")

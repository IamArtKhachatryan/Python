import os
import time
import random
from collections import Counter
from threading import Thread, Lock
from multiprocessing import Process, Manager

def create_large_file(filename, num_lines=1000, num_words_per_line=10):
    words = ["python", "data", "science", "code", "programming", "parallel", "threading", "multiprocessing", "performance"]
    with open(filename, "w") as f:
        for _ in range(num_lines):
            line = " ".join(random.choice(words) for _ in range(num_words_per_line))
            f.write(line + "\n")
    print(f"File {filename} created with {num_lines} lines.")

def count_words_sequential(filename):
    word_count = Counter()
    with open(filename, 'r') as f:
        for line in f:
            words = line.strip().split()
            word_count.update(words)
    return word_count

def count_words_threaded(filename, num_threads=4):
    word_count = Counter()
    lock = Lock()
    file_size = os.path.getsize(filename)
    chunk_size = file_size // num_threads

    def process_chunk(chunk):
        nonlocal word_count
        local_counter = Counter(chunk.strip().split())
        with lock:
            word_count.update(local_counter)

    with open(filename, 'r') as f:
        threads = []
        for _ in range(num_threads):
            chunk = f.read(chunk_size)
            if chunk:
                thread = Thread(target=process_chunk, args=(chunk,))
                threads.append(thread)
                thread.start()

        for thread in threads:
            thread.join()

    return word_count

def process_chunk(chunk, shared_dict):
    local_counter = Counter(chunk.strip().split())
    for word, count in local_counter.items():
        shared_dict[word] = shared_dict.get(word, 0) + count


def count_words_multiprocessing(filename, num_processes=4):
    word_count = Counter()
    manager = Manager()
    shared_dict = manager.dict()
    file_size = os.path.getsize(filename)
    chunk_size = file_size // num_processes

    with open(filename, 'r') as f:
        processes = []
        for _ in range(num_processes):
            chunk = f.read(chunk_size)
            if chunk:
                process = Process(target=process_chunk, args=(chunk, shared_dict))
                processes.append(process)
                process.start()

        for process in processes:
            process.join()

    return Counter(shared_dict)

def benchmark_word_counting(filename):
    start_time = time.time()
    sequential_result = count_words_sequential(filename)
    sequential_time = time.time() - start_time
    print(f"Sequential execution time: {sequential_time:.4f} seconds")

    start_time = time.time()
    threaded_result = count_words_threaded(filename)
    threaded_time = time.time() - start_time
    print(f"Multithreaded execution time: {threaded_time:.4f} seconds")

    start_time = time.time()
    multiprocessing_result = count_words_multiprocessing(filename)
    multiprocessing_time = time.time() - start_time
    print(f"Multiprocessing execution time: {multiprocessing_time:.4f} seconds")

    print("\nSpeedup (relative to sequential):")
    print(f"Multithreading speedup: {sequential_time / threaded_time:.2f}")
    print(f"Multiprocessing speedup: {sequential_time / multiprocessing_time:.2f}")

if __name__ == "__main__":
    filename = "large_text_file.txt"
    create_large_file(filename, num_lines=5000, num_words_per_line=50)

    benchmark_word_counting(filename)

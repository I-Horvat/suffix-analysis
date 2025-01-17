

import os
import time
import matplotlib.pyplot as plt
import random
import string
from SuffixArray import build_suffix_array, suffix_array_search, suffix_array_range_search, build_lcp_array, \
    find_longest_common_prefix
from SuffixTrie import SuffixTrie
import sys
import psutil

def get_memory_usage(obj):
    return sys.getsizeof(obj)
def compare_lcp_performance(test_string):
    lcp_metrics = {"suffix_array": {"time": 0, "memory": 0, "lcp": ""},
                   "suffix_trie": {"time": 0, "memory": 0, "lcp": ""}}

    start_time=time.perf_counter()
    suffix_array=build_suffix_array(test_string)
    lcp_array=build_lcp_array(test_string, suffix_array)
    max_lcp_value, lcp_string=find_longest_common_prefix(test_string, suffix_array, lcp_array)
    end_time=time.perf_counter()
    lcp_metrics["suffix_array"]["time"]=end_time-start_time
    lcp_metrics["suffix_array"]["memory"]=get_memory_usage(suffix_array)
    lcp_metrics["suffix_array"]["lcp"]=lcp_string

    trie=SuffixTrie()
    start_time=time.perf_counter()
    trie.insert(test_string)
    lcp_trie=trie.find_lcp()
    end_time=time.perf_counter()
    lcp_metrics["suffix_trie"]["time"]=end_time - start_time
    lcp_metrics["suffix_trie"]["memory"]=get_memory_usage(trie)
    lcp_metrics["suffix_trie"]["lcp"]=lcp_trie

    return lcp_metrics
def experiment():

    sizes = [100, 500, 1000, 5000]
    patterns = ["".join(random.choices(string.ascii_lowercase, k=3)) for _ in range(5)]
    prefix = random.choice(string.ascii_lowercase)

    suffix_array_metrics = {"insert_time": [], "search_time": [], "range_search_time": [], "delete_time": [],
                            "insert_memory": [], "delete_memory": []}
    suffix_trie_metrics = {"insert_time": [], "search_time": [], "range_search_time": [], "delete_time": [],
                           "insert_memory": [], "delete_memory": []}
    lcp_metrics = {"suffix_array_time": [], "suffix_array_memory": [],
                   "suffix_trie_time": [], "suffix_trie_memory": []}

    for size in sizes:
        test_string = ''.join(random.choices(string.ascii_lowercase, k=size))

        for pattern in patterns:
            insertion_point = random.randint(0, len(test_string) // 2)
            test_string = test_string[:insertion_point] + pattern + test_string[insertion_point:]

        start_time = time.perf_counter()
        suffix_array = build_suffix_array(test_string)
        suffix_array_metrics["insert_time"].append(time.perf_counter()-start_time)
        suffix_array_metrics["insert_memory"].append(get_memory_usage(suffix_array))

        start_time = time.perf_counter()
        for pattern in patterns:
            suffix_array_search(test_string, suffix_array, pattern)
        suffix_array_metrics["search_time"].append(time.perf_counter()-start_time)

        start_time = time.perf_counter()
        suffix_array_range_search(test_string, suffix_array, prefix)
        suffix_array_metrics["range_search_time"].append(time.perf_counter()-start_time)

        start_time = time.perf_counter()
        updated_string = test_string.replace(patterns[0], "")
        suffix_array = build_suffix_array(updated_string)
        suffix_array_metrics["delete_time"].append(time.perf_counter()-start_time)
        suffix_array_metrics["delete_memory"].append(get_memory_usage(suffix_array))

        trie = SuffixTrie()
        start_time = time.perf_counter()
        trie.insert(test_string)
        suffix_trie_metrics["insert_time"].append(time.perf_counter()-start_time)
        suffix_trie_metrics["insert_memory"].append(psutil.Process().memory_info().rss)

        start_time = time.perf_counter()
        for pattern in patterns:
            trie.search(pattern)
        suffix_trie_metrics["search_time"].append(time.perf_counter()-start_time)

        start_time = time.perf_counter()
        trie.range_search(prefix)
        suffix_trie_metrics["range_search_time"].append(time.perf_counter()-start_time)

        start_time = time.perf_counter()
        trie.delete(patterns[0])
        suffix_trie_metrics["delete_time"].append(time.perf_counter()-start_time)
        suffix_trie_metrics["delete_memory"].append(psutil.Process().memory_info().rss)

        lcp_comparison = compare_lcp_performance(test_string)
        lcp_metrics["suffix_array_time"].append(lcp_comparison["suffix_array"]["time"])
        lcp_metrics["suffix_array_memory"].append(lcp_comparison["suffix_array"]["memory"])
        lcp_metrics["suffix_trie_time"].append(lcp_comparison["suffix_trie"]["time"])
        lcp_metrics["suffix_trie_memory"].append(lcp_comparison["suffix_trie"]["memory"])



    output_dir = "experiment_plots"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for metric in ["insert", "search", "range_search", "delete"]:
        plt.figure(figsize=(12, 6))
        plt.plot(sizes, suffix_array_metrics[f"{metric}_time"], marker='o', label=f'Suffix Array {metric.title()} Time')
        plt.plot(sizes, suffix_trie_metrics[f"{metric}_time"], marker='o', label=f'Suffix Trie {metric.title()} Time')
        plt.xlabel("Input Size (Length of String)")
        plt.ylabel("Time (seconds)")
        plt.title(f"{metric.title()} Time: Suffix Array vs Suffix Trie")
        plt.legend()
        plt.grid()
        plt.savefig(os.path.join(output_dir, f"{metric}_time.png"))
        plt.close()

        if f"{metric}_memory" in suffix_array_metrics:
            plt.figure(figsize=(12, 6))
            plt.plot(sizes, suffix_array_metrics[f"{metric}_memory"], marker='o',
                     label=f'Suffix Array {metric.title()} Memory (Bytes)')
            plt.plot(sizes, suffix_trie_metrics[f"{metric}_memory"], marker='o',
                     label=f'Suffix Trie {metric.title()} Memory (Bytes)')
            plt.xlabel("Input Size (Length of String)")
            plt.ylabel("Memory Usage (Bytes)")
            plt.title(f"{metric.title()} Memory Usage: Suffix Array vs Suffix Trie")
            plt.legend()
            plt.grid()
            plt.savefig(os.path.join(output_dir, f"{metric}_memory_usage.png"))
            plt.close()

    plt.figure(figsize=(12, 6))
    plt.plot(sizes, lcp_metrics["suffix_array_time"], marker='o', label="Suffix Array LCP Time")
    plt.plot(sizes, lcp_metrics["suffix_trie_time"], marker='o', label="Suffix Trie LCP Time")
    plt.xlabel("Input Size (Length of String)")
    plt.ylabel("Time (seconds)")
    plt.title("LCP Time Comparison: Suffix Array vs Suffix Trie")
    plt.legend()
    plt.grid()
    plt.savefig(os.path.join(output_dir, "lcp_time_comparison.png"))
    plt.close()

    plt.figure(figsize=(12, 6))
    plt.plot(sizes, lcp_metrics["suffix_array_memory"], marker='o', label="Suffix Array LCP Memory (Bytes)")
    plt.plot(sizes, lcp_metrics["suffix_trie_memory"], marker='o', label="Suffix Trie LCP Memory (Bytes)")
    plt.xlabel("Input Size (Length of String)")
    plt.ylabel("Memory Usage (Bytes)")
    plt.title("LCP Memory Usage Comparison: Suffix Array vs Suffix Trie")
    plt.legend()
    plt.grid()
    plt.savefig(os.path.join(output_dir, "lcp_memory_comparison.png"))
    plt.close()

    print(f"Time and memory usage plots saved in '{output_dir}'")

def main():
    print("Running performance comparison experiment...")
    experiment()

if __name__ == "__main__":
    main()

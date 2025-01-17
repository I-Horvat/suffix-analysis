import sys

from SuffixArray import build_suffix_array, build_lcp_array, find_longest_common_prefix
from SuffixTrie import SuffixTrie


def visualize_experiment(test_string,string_to_delete="ana",string_to_search="ana"):
    print(f"Running visualization experiment for {test_string}...")

    trie = SuffixTrie()
    trie.insert(test_string, visualize_steps=True)
    trie.visualize("pre.gv")
    print(f"Searching for '{string_to_search}' in the trie")
    trie.search(string_to_search)
    print(f"Deleting '{string_to_delete}' from the trie")
    trie.delete(string_to_delete, visualize_steps=True)
    trie.visualize("post.gv")
    print("Visualization experiment completed")
def lcp_experiment(test_string):
    suffix_array=build_suffix_array(test_string)
    lcp_array=build_lcp_array(test_string, suffix_array)
    max_lcp_value, lcp_string=find_longest_common_prefix(test_string, suffix_array, lcp_array)
    return max_lcp_value, lcp_string

def main(test_string,string_to_delete,string_to_search):
    print("Running experiment for Suffix Array and Suffix Trie...")
    visualize_experiment(test_string,string_to_delete,string_to_search)
    max_lcp_value, lcp_string=lcp_experiment(test_string)
    print(f"Longest Common Prefix: {lcp_string} (Length: {max_lcp_value})")

if __name__ == '__main__':
    default_test_string = "banana"
    default_string_to_search = "ana"
    default_string_to_delete = "ana"

    test_string = sys.argv[1] if len(sys.argv) > 1 else default_test_string
    string_to_search = sys.argv[2] if len(sys.argv) > 2 else default_string_to_search
    string_to_delete = sys.argv[3] if len(sys.argv) > 3 else default_string_to_delete

    main(test_string, string_to_delete, string_to_search)

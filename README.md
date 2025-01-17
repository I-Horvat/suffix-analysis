# Suffix Array and Suffix Trie Analysis

This project provides Python implementations of **Suffix Array** and **Suffix Trie**, comparing their performance and memory usage for various operations. The repository includes experiments, visualizations, and datasets for a comprehensive analysis.

---

## Features

### Suffix Array
- **Operations**:
    - Build a suffix array.
    - Perform search and range search.
    - Compute the Longest Common Prefix (LCP).


### Suffix Trie
- **Operations**:
    - Insert, search, range search, and delete strings.
    - Visualize the trie at any step as `.png` files.

### Experiments
- Compare time and memory usage for:
    - Insert.
    - Search.
    - Range Search.
    - Delete.
- Generate and save plots in `experiment_plots/`.

### Visualization
- Save visualizations of the suffix trie in `.png` format for operations like insertion, search, and deletion.

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone <https://github.com/I-Horvat/suffix-analysis.git>
   cd <suffix-analysis>
   ```

2. **Create a virtual environment**:

    ```bash
    conda env create -f environment.yml
    conda activate suffix-analysis
   ```
   
## Usage
By default, the `performance_experiment.py` script runs the experiment for various input sizes of randomly generated test strings.
The `visualization_experiment.py` script visualizes the creation of a suffix trie for a given test string.
If none are provided it visualizes the creation of a suffix trie for the string "banana", searches and deletes "ana" from the trie.
The experiment also find the lcp of the suffix array of the given string or the default string "banana".


1. **Run the experiments**:
   ```bash
    python performance_experiment.py 
    python visualization_experiment.py <test_string> <search_string> <delete_string> 
    ```
   
---

from graphviz import Digraph
import os

class SuffixTrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class SuffixTrie:
    def __init__(self):
        self.root = SuffixTrieNode()

    def insert(self, s, visualize_steps=False, output_dir="visualizations"):
        if visualize_steps and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        s= s+"$"
        for i in range(len(s)):
            current = self.root
            for char in s[i:]:
                if char not in current.children:
                    current.children[char] = SuffixTrieNode()
                current = current.children[char]
            current.is_end_of_word = True

            if visualize_steps:
                self.visualize(os.path.join(output_dir, f"insert_step_{i}.gv"))

    def search(self, pattern):
        pattern = pattern + "$"
        current = self.root

        for idx, char in enumerate(pattern):
            if char not in current.children:
                return False
            current = current.children[char]
        return True

    def range_search(self, prefix):
        results=[]
        current=self.root
        prefix=prefix+"$"

        for char in prefix:
            if char not in current.children:
                return results
            current=current.children[char]

        def dfs_iterative(node, path):
            stack=[(node, path)]
            while stack:
                current_node, current_path = stack.pop()
                if current_node.is_end_of_word:
                    results.append(current_path)
                for char, child in current_node.children.items():
                    stack.append((child, current_path + char))

        dfs_iterative(current, prefix)
        return results

    def delete(self, pattern, visualize_steps=False, output_dir="visualizations"):
        if visualize_steps and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        pattern=pattern+"$"

        def dfs(node, depth):
            if depth==len(pattern):
                if not node.is_end_of_word:
                    return False
                node.is_end_of_word = False
                return len(node.children) == 0

            char=pattern[depth]
            if char not in node.children:
                return False

            should_delete_child = dfs(node.children[char], depth+1)

            if should_delete_child:
                del node.children[char]
                return len(node.children) == 0 and not node.is_end_of_word

            return False

        result=dfs(self.root, 0)
        if visualize_steps:
            self.visualize(os.path.join(output_dir, f"delete_step_{pattern}.gv"))
        return result

    def visualize(self, output_file="suffix_trie.gv"):
        graph=Digraph("Suffix Trie", format="png")

        def add_edges(node, parent_id):
            for char, child in node.children.items():
                child_id = f"{id(child)}"
                graph.node(child_id, char)
                graph.edge(parent_id, child_id)
                add_edges(child, child_id)

        root_id = f"{id(self.root)}"
        graph.node(root_id, "ROOT")
        add_edges(self.root, root_id)
        graph.render(output_file, cleanup=True)

    def find_lcp(self):
        lcp = ""
        current=self.root

        while len(current.children)==1 and not current.is_end_of_word:
            char, next_node=next(iter(current.children.items()))
            lcp+=char
            current=next_node

        return lcp

    def find_pairwise_lcp(self):
        max_lcp = ""
        stack=[(self.root, "")]

        while stack:
            node, path=stack.pop()
            if len(node.children)>1:
                if len(path)>len(max_lcp):
                    max_lcp=path
            for char, child in node.children.items():
                stack.append((child, path + char))
        return max_lcp
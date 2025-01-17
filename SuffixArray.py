import numpy as np

def build_suffix_array(s):
    suffixes=np.array([(s[i:], i) for i in range(len(s))], dtype=object)
    suffixes=np.array(sorted(suffixes, key=lambda x: x[0]), dtype=object)
    return np.array([suffix[1] for suffix in suffixes])

def build_lcp_array(s, suffix_array):
    n=len(s)
    suffix_ranks=np.zeros(n, dtype=int)
    lcp_array=np.zeros(n, dtype=int)

    for index, suffix_index in enumerate(suffix_array):
        suffix_ranks[suffix_index]=index

    common_prefix_length=0
    for i in range(n):
        if suffix_ranks[i]==n-1:
            common_prefix_length=0
            continue
        next_suffix_index=suffix_array[suffix_ranks[i]+1]
        while (i+common_prefix_length<n and
               next_suffix_index+common_prefix_length<n and
               s[i+common_prefix_length]==s[next_suffix_index+common_prefix_length]):
            common_prefix_length+=1
        lcp_array[suffix_ranks[i]]=common_prefix_length
        if common_prefix_length>0:
            common_prefix_length-=1
    return lcp_array

def suffix_array_search(s, suffix_array, pattern):
    left, right=0, len(suffix_array)-1
    while left<=right:
        mid=(left+right)//2
        suffix=s[suffix_array[mid]:]
        if suffix.startswith(pattern):
            return True
        elif suffix<pattern:
            left=mid+1
        else:
            right=mid-1
    return False

def suffix_array_range_search(s, suffix_array, prefix):
    left, right = 0, len(suffix_array)-1
    matching_indices = []

    while left <= right:
        mid=(left + right)//2
        suffix = s[suffix_array[mid]:]
        if suffix.startswith(prefix):
            matching_indices.append(suffix_array[mid])
            left_ptr, right_ptr = mid-1, mid+1
            while left_ptr>=0 and s[suffix_array[left_ptr]:].startswith(prefix):
                matching_indices.append(suffix_array[left_ptr])
                left_ptr-=1
            while right_ptr<len(suffix_array) and s[suffix_array[right_ptr]:].startswith(prefix):
                matching_indices.append(suffix_array[right_ptr])
                right_ptr+=1
            break
        elif suffix < prefix:
            left=mid+1
        else:
            right=mid-1
    return sorted(matching_indices)

def find_longest_common_prefix(s, suffix_array, lcp_array):
    max_lcp_value=max(lcp_array)
    if max_lcp_value==0:
        return 0, ""

    max_lcp_index=np.argmax(lcp_array)
    start_index=suffix_array[max_lcp_index]
    lcp_string=s[start_index:start_index+max_lcp_value]

    return max_lcp_value, lcp_string

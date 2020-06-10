def suffix_seq(s):
    for i in range(len(s)):
        yield s[i:]
        
def suffix_map(s, suff_arr=None):
    return([s[i:] for i in suff_arr] if suff_arr
      else sorted(suffix_seq(s)))

def bin_find(strs, qstr, lr):
    l = 0
    r = len(strs)
    while l + 1 != r:
        m = (r - l) // 2 + l
        if qstr < strs[m]:
            r = m
        else:
            l = m
    return r if lr == 'l' else l

def len_lcp(s1, s2):
    length = 0
    for c1,c2 in zip(s1,s2):
        if c1 == c2:
            length += 1
        else:
            break
    return length
            
def lcp_find(strs, qstr, lr):
    l = 0; r = len(strs)# - 1
    lcp_l = lcp_r = min_lcp = 0
    while l + 1 != r:
        m = (r - l) // 2 + l
        min_lcp = min(lcp_l, lcp_r)
        qstring = qstr[min_lcp:]
        string = strs[m][min_lcp:]
        if qstring < string:
            r = m
            lcp_r = min_lcp + len_lcp(qstring, string)
        else:
            l = m
            lcp_l = min_lcp + len_lcp(qstring, string)
    return r if lr == 'l' else l

def suff_count(suffixes, qstr, find=bin_find):
    l = qstr + '#'; r = qstr + '~'
    return find(suffixes, r, 'r') - find(suffixes, l, 'l') + 1

def basic_counts(string, qstr):
    occur_idxes = set()
    for beg in range(len(string)):
        idx = string.find(qstr, beg)
        if idx != -1:
            occur_idxes.add(idx)
    return len(occur_idxes)


with open('dna.txt') as inp:
    inp.readline() # IGNORE
    string = inp.readline()
    suff_arr = list(map(int, inp.readline().split()))
    inp.readline() # IGNORE
    inp.readline() # IGNORE
    qstrs = inp.read().splitlines()

    '''
    print(string)
    print(suff_arr, len(suff_arr))
    print(qstrs)
    print(len(string)) # str + $(1)
    '''

import time
from tqdm import tqdm

suff_map = suffix_map(string, suff_arr)


print('-------------------')
s = time.time()
suff_map = suffix_map(string, suff_arr)
for qstr in tqdm(qstrs):
    sc = suff_count(suff_map, qstr, bin_find)
    #if bc != sc: print(bc, sc)
t = time.time()
print('basic suffix array:', t - s)

print('-------------------')
s = time.time()
suff_map = suffix_map(string, suff_arr)
for qstr in tqdm(qstrs):
    sc = suff_count(suff_map, qstr, lcp_find)
    #if bc != sc: print(bc, sc)
t = time.time()
print(t - s)
print(' lcp suffix array:', t - s)

print('-------------------')
s = time.time()
for qstr in tqdm(qstrs):
    bc = basic_counts(string, qstr)
t = time.time()
print('             basic:', t - s)

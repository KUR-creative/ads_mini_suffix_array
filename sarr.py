import itertools as I
import funcy as F

def window(seq, n=2):
    '''
    Returns a sliding window (of width n) over data from the iterable
    s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ... 
    '''
    it = iter(seq)
    result = tuple(I.islice(it, n))
    if len(result) == n:
        #yield ''.join(result)
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        #yield ''.join(result)
        yield result
print(list(window([1,2,3,4,5])))
exit()
        
def uniques(string, size, search_mode=False):
    qstrs = list(window(string, size))
    ret = []
    qset = set()
    for start, qstr in enumerate(qstrs):
        if(qstr not in qset and
           string.find(qstr, start+1) == -1):
            if search_mode:
                return True
            else:
                ret.append(qstr)
        qset.add(qstr)
    return False if search_mode else ret

def bin_answer(dna):
    max_size = len(dna)
    min_size = 0
    while min_size + 1 != max_size:
        mid_size = min_size + (max_size - min_size) // 2
        mid_uniq = uniques(dna, mid_size, search_mode=True)
        if mid_uniq:
            max_size = mid_size
        else:
            min_size = mid_size
    qstrs = uniques(dna, max_size)
    qstrs.sort()
    return qstrs[0]

string = 'abaab$'
def suffix_seq(s):
    for i in range(len(s)):
        yield s[i:]

def suffix_map(s, suff_arr=None):
    return([s[i:] for i in suff_arr] if suff_arr
      else sorted(suffix_seq(s)))

tup = lambda f: lambda argtup: f(*argtup)
def suffix_arr(s):
    sorted_suffixes = sorted(
        enumerate(suffix_seq(s)),
        key=tup(lambda i,k: [k,i]))
    return sorted_suffixes
    #return F.lmap(F.first, sorted_suffixes)
print(list(suffix_seq(string)))
print(suffix_map(string))
idxes = F.lmap(F.first, suffix_arr(string))
suffixes = F.lmap(F.second, suffix_arr(string))
print(idxes)
print(suffixes)
print(suffix_map(string, idxes))
    
#exit()

qstr = 'a'
# m 1

def basic_counts(string, qstr):
    occur_idxes = set()
    for beg in range(len(string)):
        idx = string.find(qstr, beg)
        if idx != -1:
            occur_idxes.add(idx)
    return len(occur_idxes)

#import re p = re.compile('aba')
#print(p.findall('abababa$'))
print(basic_counts('abababa$', 'aba'))

print(suffix_map('abba$'))
print(suffix_arr('abbaba$'))

def f(l,r, rl):
    return (r - l) // 2 + (l if rl == 'l' else r)

print(f(2, 4, 'l'))

string = 'abbaba$'
suffixes = suffix_map(string)

def bin_find(strs, qstr):
    l = 0
    r = len(strs) - 1
    while l + 1 != r:
        m = (r - l) // 2 + l
        #print('---------'); print(qstr); print(strs[m]); print(qstr < strs[m]); print(l,r,m, end=' -> ');
        if qstr < strs[m]:
            r = m
        else:
            l = m
        #print(l,r,m)
    return l

def suff_count(suffixes, qstr):
    left = qstr + '#'
    right = qstr + '~'
    return bin_find(suffixes, right) - bin_find(suffixes, left)

print(suff_count(suffixes, 'ba'))

from pprint import pprint
print('---- aababa$ ----')
pprint(suffix_arr('aababa$'))

print('---- baabaabbaa$ ----')
pprint(suffix_arr('baabaabbaa$'))
print([x for x,_ in suffix_arr('aababa$')])

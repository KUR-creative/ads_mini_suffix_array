def suffix_seq(s):
    for i in range(len(s)):
        yield s[i:]
        
def suffix_map(s, suff_arr=None):
    return([s[i:] for i in suff_arr] if suff_arr
      else sorted(suffix_seq(s)))

def bin_find(strs, qstr, lr): # lr = 'l' or 'r'
    #print('---------', lr, '---------'); print('l m r')
    l = 0
    r = len(strs)# - 1
    while l + 1 != r:
        m = (r - l) // 2 + l
        #print(l,m,r, qstr, strs[m], qstr < strs[m])
        if qstr < strs[m]:
            r = m
        else:
            l = m
        #print(l,m,r)
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
    #print('---------', lr, '---------'); print('l m r')
    l = 0; r = len(strs)# - 1
    lcp_l = lcp_r = min_lcp = 0
    while l + 1 != r:
        m = (r - l) // 2 + l
        #print('----')
        #print(l,m,r, '|', lcp_l, lcp_r, min_lcp, '|', qstr, strs[m], qstr < strs[m])
        min_lcp = min(lcp_l, lcp_r)
        qstring = qstr[min_lcp:]
        string = strs[m][min_lcp:]
        #if qstr[min_lcp:] < strs[m][min_lcp:]:
        if qstring < string:
            r = m
            #lcp_r = min_lcp + len_lcp(qstr[min_lcp], strs[m])
            lcp_r = min_lcp + len_lcp(qstring, string)
        else:
            l = m
            lcp_l = min_lcp + len_lcp(qstring, string)
        #print(l,m,r, '|', lcp_l, lcp_r, min_lcp, '|', qstr, strs[m], qstr < strs[m])
        #print(l,m,r, '|', lcp_l, lcp_r, min_lcp, '|', qstring, string, qstring < string)
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

'''
#s,qstr=['aaaa$', 'aa']
s,qstr = ['aaaaaaaaaaaac$', 'aaaaaac']
print(basic_counts(s, qstr))
print(suff_count(suffix_map(s), qstr, lcp_find))

from pprint import pprint
pprint(suffix_map('aaaaaaaaaa$'))
'''
'''
print(suffix_map(s))

tup = lambda f: lambda argtup: f(*argtup)
def suffix_arr(s):
    sorted_suffixes = sorted(
        enumerate(suffix_seq(s)),
        key=tup(lambda i,k: [k,i]))
    return sorted_suffixes
pprint(suffix_arr('baabaabbaa$'))
print(basic_counts('baabaabbaa$', 'aabb'))

pprint(suffix_arr('aaaaa$'))
print(basic_counts('aaaaa$', 'aaa'))
'''

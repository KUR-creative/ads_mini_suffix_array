from bidict import bidict
import funcy as F
import itertools as I

tup = lambda f: lambda argtup: f(*argtup)
def unzip(seq):
    return zip(*seq)

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
        
#------------------- naive implementations ---------------------
def suffix_seq(s):
    for i in range(len(s)):
        yield s[i:]

def naive_suffix_map(s):
    sorted_suffixes = sorted(
        enumerate(suffix_seq(s)),
        key=tup(lambda i,k: [k,i]))
    return sorted_suffixes

#---------------------- DC3 implementation ---------------------
def int_map(alphabet):
    return dict((s,i) for i,s in enumerate(sorted(alphabet)))

def pad3x(ints, padval=0):
    num_pad = (3 - len(ints) % 3) % 3
    return ints + [padval] * num_pad

def origin_indexes(length):
    return (
        list(range(0,length,3)),
        list(range(1,length,3)),
        list(range(2,length,3))
    )

def suffix_array(imap, string):
    #[1] Get index lists, reduced string
    unsorted_s0idx, s1idx, s2idx = origin_indexes(len(string))
    rs = pad3x([imap[c] for c in string]) + [0,0,0] #reduced string
    s1s2 = s1idx + s2idx
    #print(unsorted_s0idx, s1idx, s2idx)
    #print('   rs:',rs)
    
    #[2] Get (flawed) s1+s2 suffix array. ordered by (flawed) rank
    # It can't be SA if some elems are duplicated.
    # Because it can't allow duplicated elem.. 
    s12_sa = sorted(s1s2, key=lambda i: rs[i:i+3])
    #print('s12_sa:', s12_sa)

    #[3] Check uniqueness of elems and get rank ordered by s12_sa
    all_unique = True
    s12_rank = [0]
    rank = 0
    for idx0,idx1 in window(s12_sa):
        # Check 3chars of s12_sa duplication pairwisely.
        if rs[idx0:idx0+3] == rs[idx1:idx1+3]:
            all_unique = False
        else:
            rank += 1
        s12_rank.append(rank)
    #print('all_unique:', all_unique)
    #print(s12_rank)
    
    #[4] Get rank and SA (s1-s2 ordered) if all elems are unique
    s12_sa2rank = dict(zip(s12_sa, s12_rank))
    if not all_unique:
        #[4.1] Get rank from recur call.
        next_string = F.lmap(s12_sa2rank, s1s2)
        next_imap = int_map(set(next_string))
        s12_rank = suffix_array(next_imap, next_string)
        
        # Change s12_sa2rank, s12_sa
        s12_sa2rank = dict(zip(s1s2, s12_rank))
        s12_sa = F.lmap(F.first, sorted(
            s12_sa2rank.items(),
            key=tup(lambda sa, rank: rank)
        ))
        #print('s12_sa:', s12_sa)
        #print('s12_sa2rank:', s12_sa2rank)
        
    s0_sa = sorted(
        unsorted_s0idx,
        key=lambda i: [rs[i], s12_sa2rank.get(i+1, 0)])
    #print(' 0idx:', s0_sa)

    #[5] if unique, merge with s0!
    len_s1s2 = len(s12_sa)
    len_s0 = len(s0_sa)
    len_sa = len_s1s2 + len_s0
    suff_arr = []
    i12 = i0 = 0
    #print('----')
    while i12 + i0 < len_sa:
        beg = s12_sa[i12]
        Sno = beg % 3
        beg0 = s0_sa[i0]
        # make form for comparison
        form12 = [*rs[beg:beg+Sno], s12_sa2rank.get(beg+Sno, 0)]
        form0 = [*rs[beg0:beg0+Sno], s12_sa2rank.get(beg0+Sno, 0)]
        assert len(form12) == len(form0), \
            f'form12 = {form12} != {form0} = form0'
        #print(form12, form0)
        if form12 < form0:
            suff_arr.append(beg)
            i12 += 1
        elif form12 > form0:
            suff_arr.append(beg0)
            i0 += 1
        else:
            assert False, 'do not reach'
        #print(Sno, '|', i12, i0, ':', len_s1s2, len_s0, '|', beg, beg0, '|', form12, form0)
        #print(suff_arr)
        if i0 == len_s0:
            suff_arr = suff_arr + s12_sa[i12:]
            break
        if i12 == len_s1s2:
            suff_arr = suff_arr + s0_sa[i0:]
            break
    return suff_arr
    
imap = int_map('ab$')
string = 'aa$'
string = 'aaa$'
#imap = int_map('ac$'); string = 'aac$'
#string = 'aababa$'
imap = int_map('acgt$'); string = 'acccc$'

print('actual:', suffix_array(imap, string))
print('expect:', [x for x,_ in naive_suffix_map(string)])

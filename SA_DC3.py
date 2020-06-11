import itertools as I

tup = lambda f: lambda argtup: f(*argtup)

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

def origin_indexes(string):
    l = len(string)
    return (
        list(range(0,l,3)),
        list(range(1,l,3)),
        list(range(2,l,3))
    )

def suffix_array(imap, string):
    unsorted_s0idx, s1idx, s2idx = origin_indexes(string)
    #print(unsorted_s0idx, s1idx, s2idx)

    rs = pad3x([imap[c] for c in string]) + [0,0,0] #reduced string
    #print('   rs:',rs)

    # index of origin string. part of SA
    # index of s1s2idx is grade(nth). (sorted)
    s1s2idx = sorted( 
        s1idx + s2idx, 
        key=lambda i: rs[i:i+3])
    # we can know s1 or s2 by calculating modular of index.
    #print([rs[i:i+3] for i in s1idx + s2idx])
    print('12idx:', s1s2idx)


    # inverse mapping of s1s2idx. part of inverse SA
    s1s2nth = dict((s,i) for i,s in enumerate(s1s2idx))
    #print('12nth:', s1s2nth)
    
    # indexes of origin string, sorted by s0. part of SA. 
    s0idx = sorted(
        unsorted_s0idx, key=lambda i: [rs[i], s1s2nth.get(i+1, 0)])

    #print(' 0idx:', s0idx)

    #(if s1s2idx values are distinct,) merge with s0
    len_s1s2 = len(s1s2idx)
    len_s0 = len(s0idx)
    len_sa = len_s1s2 + len_s0
    suff_arr = []
    i12 = i0 = 0
    
    #print('----')
    while i12 + i0 < len_sa:
        beg = s1s2idx[i12]
        Sno = beg % 3
        beg0 = s0idx[i0]
        
        # make form for comparison
        form12 = [*rs[beg:beg+Sno], s1s2nth.get(beg+Sno, 0)]
        form0 = [*rs[beg0:beg0+Sno], s1s2nth.get(beg0+Sno, 0)]
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
            suff_arr = suff_arr + s1s2idx[i12:]
            break
        if i12 == len_s1s2:
            suff_arr = suff_arr + s0idx[i0:]
            break

    #print('ans:', suff_arr)
    return suff_arr

    #s0idx = # ordered by s1
    #[5, 1, 4, 2]
    #s1s2nth = [
    
imap = int_map('ab$')
#string = 'aa$'
#string = 'aaa$'
#string = 'aababa$'
imap = int_map('acgt$'); string = 'acccc$'

print(suffix_array(imap, string))
print([x for x,_ in naive_suffix_map(string)])

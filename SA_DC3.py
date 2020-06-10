from bidict import bidict

def int_map(alphabet):
    return bidict((s,i) for i,s in enumerate(sorted(alphabet)))

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

imap = int_map('ab$')
string = 'aababa$'

def suffix_array(imap, string):
    unsorted_s0idx, s1idx, s2idx = origin_indexes(string)
    #print(unsorted_s0idx, s1idx, s2idx)

    rs = pad3x([imap[c] for c in string]) #reduced string
    #print(rs)

    # index of origin string. part of SA
    # index of s1s2idx is grade(nth). (sorted)
    s1s2idx = sorted( 
        s1idx + s2idx, 
        key=lambda i: rs[i:i+3])
    # we can know s1 or s2 by calculating modular of index.

    # inverse mapping of s1s2idx. part of inverse SA
    s1s2nth = dict((s,i) for i,s in enumerate(s1s2idx))
    
    # we can check 3chars of s1s2idx duplication pairwisely.
    # if unique, merge with s0!
    # if not, make s1s2idx, s1s2nth by recursing suffix_array

    # indexes of origin string, sorted by s0. part of SA. 
    s0idx = sorted(
        unsorted_s0idx, key=lambda i: [rs[i], s1s2nth.get(i+1, 0)])

    #print(s1s2idx)
    #print(s0idx)

    #(if s1s2idx values are distinct,) merge with s0
    len_s1s2 = len(s1s2idx)
    len_s0 = len(s0idx)
    len_sa = len_s1s2 + len_s0
    suff_arr = []
    i12 = i0 = 0
    #print('----', len_sa)
    while i12 + i0 < len_sa:
        beg = s1s2idx[i12]
        mod = beg % 3
        beg0 = s0idx[i0]
        
        # make form for comparison
        form12 = [*rs[beg:beg+mod], s1s2nth.get(beg+mod, 0)]
        form0 = [*rs[beg0:beg0+mod], s1s2nth.get(beg0+mod, 0)]
        assert len(form12) == len(form0)
        
        #print(form12, form0)
        if form12 < form0:
            suff_arr.append(beg)
            i12 += 1
        elif form12 > form0:
            suff_arr.append(beg0)
            i0 += 1
        else:
            assert False, 'do not reach'

        if i0 == len_s0:
            suff_arr = suff_arr + s1s2idx[beg:]
            break
        if i12 == len_s1s2:
            suff_arr = suff_arr + s0idx[beg0:]
            break

    #print('ans:', suff_arr)
    return suff_arr

    #s0idx = # ordered by s1
    #[5, 1, 4, 2]
    #s1s2nth = [
print(suffix_array(imap, string))

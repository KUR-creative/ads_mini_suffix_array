from bidict import bidict

def int_map(alphabet):
    return bidict((s,i) for i,s in enumerate(sorted(alphabet)))

def ints(imap, s):
    return [imap[c] for c in s]

def pad3x(ints, padval=0):
    num_pad = (3 - len(ints) % 3) % 3
    return ints + [0] * num_pad

imap = int_map('ab$')
print(ints(imap, 'aababa$'))
print('----')
print(pad3x([1]))
print(pad3x([1,1]))
print(pad3x([1,1,1]))

string = 'aababa$'

# mapping arrays
#S0idx = # index in T(original string)
#S0nth

def origin_indexes(string):
    l = len(string)
    return (
        list(range(0,l,3)),
        list(range(1,l,3)),
        list(range(2,l,3))
    )

unsorted_s0idx, s1idx, s2idx = origin_indexes(string)
print('--------')
print(unsorted_s0idx, s1idx, s2idx)

rs = pad3x([imap[c] for c in string]) #reduced string
print(rs)

# index of origin string. part of SA
# index of s1s2idx is grade(nth). (sorted)
s1s2idx = sorted( 
    s1idx + s2idx, 
    key=lambda i: rs[i:i+3])
# we can know s1 or s2 by calculating modular of index.
# we can check 3chars of s1s2idx duplication pairwisely.
# if unique, merge with s0!

# inverse mapping of s1s2idx. part of inverse SA
s1s2nth = dict((s,i) for i,s in enumerate(s1s2idx))

# indexes of origin string, sorted in s0. part of SA. 
s0idx = sorted(
    unsorted_s0idx, key=lambda i: [rs[i], s1s2nth.get(i+1, 0)])

#(if s1s2idx values are distinct,) merge with s0
#def merge(
print(s1s2idx)
print(s0idx)

len_s1s2 = len(s1s2idx)
len_s0 = len(s0idx)
len_sa = len_s1s2 + len_s0
suffix_array = []
i12 = i0 = 0
#i0 = 3
print('----', len_sa)
while i12 + i0 < len_sa:
    beg = s1s2idx[i12]
    mod = beg % 3
    beg0 = s0idx[i0]
    # make form for comparison
    form12 = [*rs[beg:beg+mod], s1s2nth.get(beg+mod, 0)]
    form0 = [*rs[beg0:beg0+mod], s1s2nth.get(beg0+mod, 0)]
    assert len(form12) == len(form0)
    print(form12, form0)
    if form12 < form0:
        suffix_array.append(beg)
        i12 += 1
    elif form12 > form0:
        suffix_array.append(beg0)
        i0 += 1
    else:
        assert False, 'do not reach'

    if i0 == len_s0:
        suffix_array = suffix_array + s1s2idx[beg:]
        break
    if i12 == len_s1s2:
        suffix_array = suffix_array + s0idx[beg0:]
        break

print('ans:', suffix_array)

#s0idx = # ordered by s1
#[5, 1, 4, 2]
#s1s2nth = [

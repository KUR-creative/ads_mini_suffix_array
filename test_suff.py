import random

from hypothesis import given, example
from hypothesis import strategies as st

from suff import *

@st.composite
def gen(draw):
    string = draw(st.text('atgc', min_size=10))#, max_size=20))
    s = random.randint(0, len(string)-1)
    t = random.randint(s+1, len(string)+1)
    return [string + '$', string[s:t]]
    
tup = lambda f: lambda argtup: f(*argtup)
#import pytest @pytest.mark.timeout(5000)
@given(gen())
@example(['aaac$', 'aac'])
def test_(s_qstr):
    s, qstr = s_qstr
    assert basic_counts(s, qstr) == suff_count(suffix_map(s), qstr)
    #if s == qstr: assert False
    
@given(gen())
def test_(s_qstr):
    s, qstr = s_qstr
    assert (basic_counts(s, qstr) ==
            suff_count(suffix_map(s), qstr, bin_find) == 
            suff_count(suffix_map(s), qstr, lcp_find))

@st.composite
def gen_s1s2ans(draw):
    lcp = draw(st.text('atgc', min_size=1))#, max_size=20))
    s1 = lcp + '-' + draw(st.text('atgc', min_size=1))
    s2 = lcp + '+' + draw(st.text('atgc', min_size=1))
    return [s1, s2, len(lcp)]

@given(gen_s1s2ans())
def test_len_lcp(s1s2ans):
    s1,s2,actual = s1s2ans
    assert len_lcp(s1,s2) == actual

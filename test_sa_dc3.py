from hypothesis import given, example
from hypothesis import strategies as st

from SA_DC3 import *

@given(st.text('atgc', min_size=1).map(lambda s: s + '$'))
def test_dc3(s):
    imap = int_map('atgc$')
    assert suffix_array(imap, s) == [x for x,_ in naive_suffix_map(s)]

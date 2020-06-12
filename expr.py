'''
Experiments for correctness and time complexity
'''
import random

from SA_DC3 import *


alphabet = 'acgt'
print(''.join(random.choices(alphabet, k=6)))

# Check special cases
def assert_eq_with_naive(s, msg):
    naive_sa = [x for x,_ in naive_suffix_map(s)]
    sa = suffix_array(int_map(s), s)
    assert naive_sa == sa, msg + f'naive = {naive_sa} != {sa} = DC3'
    
def check_special_cases():
    assert_eq_with_naive('aa$', 'No recur case 1, ')
    assert_eq_with_naive('aaa$', 'No recur case 2')
    assert_eq_with_naive('aac$', 'No recur case 3')
    assert_eq_with_naive('aababa$', 'No recur case 4')
    assert_eq_with_naive('acccc$', 'Recur case with returned SA = inverse SA')
    assert_eq_with_naive('aaccccc$', 'Recur case with returned SA != inverse SA')
    
check_special_cases()
#for N in range(10,

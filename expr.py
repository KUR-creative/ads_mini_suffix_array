''' Experiments for correctness and time complexity '''
import random
from time import time

from tqdm import tqdm
import matplotlib.pyplot as plt

from SA_DC3 import *


# Check special cases
def assert_eq_with_naive(s, msg, fast_algo=suffix_array):
    ''' If you want to test other algorithm, change fast_algo '''
    naive_sa = [x for x,_ in naive_suffix_map(s)]
    sa = fast_algo(int_map(s), s)
    assert naive_sa == sa, msg + f'naive = {naive_sa} != {sa} = DC3'
    
# Check special cases
assert_eq_with_naive('aa$', 'No recur case 1, ')
assert_eq_with_naive('aaa$', 'No recur case 2')
assert_eq_with_naive('aac$', 'No recur case 3')
assert_eq_with_naive('aababa$', 'No recur case 4')
assert_eq_with_naive('acccc$', 'Recur case with returned SA = inverse SA')
assert_eq_with_naive('aaccccc$', 'Recur case with returned SA != inverse SA')

Ns = []
naive_run_times = []
fast_run_times = []
fast_algo = suffix_array # If you want to test other algorithm, change fast_algo
min_N = 10
max_N = 200000
#step = 10000
step = 5000
overturn_N = None
overturn_idx = None
alphabet = 'acgt'
for N in tqdm(range(min_N, max_N, step)):
    Ns.append(N)
    s = ''.join(random.choices(alphabet, k=N)) + '$'
    
    beg = time()
    naive_sa = [x for x,_ in naive_suffix_map(s)]
    end = time()
    naive_run_times.append(end - beg)
    
    try:
        beg = time()
        sa = fast_algo(int_map(s), s)
        end = time()
    except Exception as e:
        print(e)
        print(f'inp: {s}')
    finally:
        fast_run_times.append(end - beg)

    if(overturn_N is None and
       naive_run_times[-1] > fast_run_times[-1]):
        overturn_N = N
        overturn_idx = len(Ns) - 1
        
    assert naive_sa == sa, \
        f' input:{s} \n naive = {naive_sa} != {sa} = DC3'

plt.plot(Ns, naive_run_times, color='b', label='naive SA algo running time')
plt.plot(Ns, fast_run_times, color='r', label='fast SA algo running time')

plt.xlabel('length of string')
plt.ylabel('running time(sec)')

plt.legend()
plt.show()

print(f'DC3 algorithm is fast after N >= {overturn_N}')

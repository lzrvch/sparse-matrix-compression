import numpy as np
from scipy.stats import mode
from itertools import product

# %%

def relative_index_coding(array, maximal_int=7):
    zeros_counter = 0
    diff_array = []
    sign_array = []
    value_array = []
    skip_next = False

    for index, item in enumerate(array):
        if item == 0:
            if skip_next:
                skip_next = False
                continue
            zeros_counter += 1
            if zeros_counter == maximal_int:
                if index < (len(array)  - 1):
                    if array[index+1] != 0:
                        value_array.append(array[index+1])
                        sign_array.append(0)
                    else:
                        sign_array.append(1)
                    skip_next = True
                    diff_array.append(zeros_counter)
                    zeros_counter = 0
                # elif index == (len(array) - 1):
                #     # sign_array.append(1)
                #     diff_array.append(zeros_counter)
                continue
            if index < (len(array) - 1) and array[index+1] != 0:
                diff_array.append(zeros_counter)
                value_array.append(array[index+1])
                zeros_counter = 0
                skip_next = True
            #if index == (len(array) - 1):
            #    diff_array.append(zeros_counter)
        else:
            if not skip_next:
                diff_array.append(0)
                value_array.append(array[index])
            skip_next = False

    return np.array(value_array), np.array(diff_array), np.array(sign_array)

# %%

def bits_for_storage(sparse_array, maximal_diff_int, bits_per_element,
                     inverse_coding=False, add_bit_for_coding_scheme=False):
    if inverse_coding:
        sparse_array = [0 if value != 0 else 1 for value in sparse_array]
    value, diff, sign = relative_index_coding(sparse_array, maximal_int=maximal_diff_int)
    if len(diff) > 0:
        bits_required = len(diff) * bits_per_element + len(sign)
        if add_bit_for_coding_scheme:
            bits_required += 1
        return bits_required
    else:
        return 1

# %%

def gen_random_sparse_array(size, rate=0.5):
    p = np.random.uniform(0, 1, size=size)
    return np.array([0 if value < rate else 1 for value in p])

# %%

def relative_index_decoding(value, diff, sign, target_len, maximal_int=7):
    decoded_array = []
    sign_index = 0
    value_index = 0
    for diff_value in diff:
        if diff_value > 0:
            decoded_array += diff_value * [0]
        if diff_value == maximal_int:
            if len(decoded_array) < target_len:
                if sign[sign_index] == 0:
                    if value_index < len(value):
                        decoded_array += [value[value_index]]
                        value_index += 1
                else:
                    decoded_array += [0]
                sign_index += 1
        else:
            if value_index < len(value):
                decoded_array += [value[value_index]]
                value_index += 1

    return decoded_array

# %%

relative_index_coding([0, 0, 0, 0, 0, 0, 0, 0, 1, 1])
v, d, s = relative_index_coding([0, 0, 0, 0, 0, 0, 0, 0, 1, 1])
relative_index_decoding(v, d, s, target_len=10)

# %%

size = 100
for _ in range(1000):
    a = gen_random_sparse_array(size, rate=0.5)
    v, d, s = relative_index_coding(a, maximal_int=1)
    if not np.array_equal(relative_index_decoding(v, d, s, target_len=size, maximal_int=1), a):
        print(a)

# %%

bits_per_element = 1
maximal_diff_int = 2 ** bits_per_element - 1
bits_for_storage(gen_random_sparse_array(1000, rate=0.5),
                 maximal_diff_int,
                 bits_per_element,
                 inverse_coding=False)

# %%

bits_per_element = 1
maximal_diff_int = 2 ** bits_per_element - 1

array = gen_random_sparse_array(1000, rate=0.5)
num_bits = 0
interval = 4
for interval_index in range(int(array.shape[0] / interval)):
    num_bits += bits_for_storage(array[interval_index*interval:(interval_index+1)*interval],
                     maximal_diff_int,
                     bits_per_element)

num_bits

# %%

bits_per_element = 2
maximal_diff_int = 2 ** bits_per_element - 1

array = gen_random_sparse_array(1000, rate=0.5)
num_bits = 0
interval = 8
for interval_index in range(int(array.shape[0] / interval)):
    sub_interval = array[interval_index*interval:(interval_index+1)*interval]
    if np.mean(sub_interval) <= 0.5:
    # if interval_index % 2 == 0:
        b = bits_for_storage(sub_interval,
                         maximal_diff_int,
                         bits_per_element)
    else:
        b = bits_for_storage(sub_interval,
                         maximal_diff_int,
                         bits_per_element,
                         inverse_coding=True)
        # b += 1
    num_bits += b

num_bits

# %%

bits_per_element = 1
maximal_diff_int = 2 ** bits_per_element - 1
array = gen_random_sparse_array(1000, rate=0.5)
val, diff, sign = relative_index_coding(array, maximal_int=maximal_diff_int)
bits_per_element * diff.shape[0] + sign.shape[0]

np.mean(diff)

diff.shape
sign.shape

# %%

bits_per_element = 1
maximal_diff_int = 2 ** bits_per_element - 1
array = gen_random_sparse_array(1000, rate=0.5)

interval = 4
full_diff = []
full_sign = []

for interval_index in range(int(array.shape[0] / interval)):
    sub_interval = array[interval_index*interval:(interval_index+1)*interval]
    diff, val, sign = relative_index_coding(sub_interval, maximal_int=maximal_diff_int)
    full_diff += list(diff)
    full_sign += list(sign)

full_diff = np.array(full_diff)
full_sign = np.array(full_sign)

# %%

len(full_diff) + len(full_sign)

# %%

full_diff.shape[0]
full_diff = np.array([0 if val > 0 else 1 for val in full_diff])
1 - np.mean(full_diff)

# %%

interval = 4
full_diff2 = []
full_sign2 = []
for interval_index in range(int(full_diff.shape[0] / interval)):
    sub_interval = full_diff[interval_index*interval:(interval_index+1)*interval]
    diff2, val, sign2 = relative_index_coding(sub_interval, maximal_int=maximal_diff_int)
    full_diff2 += list(diff2)
    full_sign2 += list(sign2)

full_diff2 = np.array(full_diff2)
full_sign2 = np.array(full_sign2)

# %%

len(full_diff2) + len(full_sign2)

# %%

full_sign.shape[0]
1 - np.mean(full_sign)

# %%

interval = 4
full_diff3 = []
full_sign3 = []
for interval_index in range(int(full_sign.shape[0] / interval)):
    sub_interval = full_sign[interval_index*interval:(interval_index+1)*interval]
    diff3, val, sign3 = relative_index_coding(sub_interval, maximal_int=maximal_diff_int)
    full_diff3 += list(diff3)
    full_sign3 += list(sign3)

full_diff3 = np.array(full_diff3)
full_sign3 = np.array(full_sign3)

# %%

len(full_diff3) + len(full_sign3)

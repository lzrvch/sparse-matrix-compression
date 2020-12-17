import numpy as np
from scipy.stats import mode
from itertools import product


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
                if index < (len(array) - 1):
                    if array[index + 1] != 0:
                        value_array.append(array[index + 1])
                        sign_array.append(0)
                    else:
                        sign_array.append(1)
                    skip_next = True
                    diff_array.append(zeros_counter)
                    zeros_counter = 0
                elif index == (len(array) - 1):
                     # sign_array.append(1)
                    diff_array.append(zeros_counter)
                continue
            if index < (len(array) - 1) and array[index + 1] != 0:
                diff_array.append(zeros_counter)
                value_array.append(array[index + 1])
                zeros_counter = 0
                skip_next = True
            if index == (len(array) - 1):
                diff_array.append(zeros_counter)
        else:
            if not skip_next:
                diff_array.append(0)
                value_array.append(array[index])
            skip_next = False

    return np.array(value_array), np.array(diff_array), np.array(sign_array)


def bits_for_storage(
    sparse_array,
    maximal_diff_int,
    bits_per_element,
    inverse_coding=False,
    add_bit_for_coding_scheme=False,
):
    if inverse_coding:
        sparse_array = [0 if value != 0 else 1 for value in sparse_array]
    value, diff, sign = relative_index_coding(
        sparse_array, maximal_int=maximal_diff_int
    )
    if len(diff) > 0:
        bits_required = len(diff) * bits_per_element + len(sign)
        if add_bit_for_coding_scheme:
            bits_required += 1
        return bits_required
    else:
        return 1


def gen_random_sparse_array(size, rate=0.5):
    p = np.random.uniform(0, 1, size=size)
    return np.array([0 if value < rate else 1 for value in p])


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

import sys
import numpy as np
import numba

yuki_num , kijun = map(int,sys.stdin.readline().split())
yuki_tall = list(map(int,sys.stdin.readline().split()))

@numba.jit(nopython=True)
def yuki(yuki_num , kijun , yuki_tall , result):
    if result == -1:
        return

    yuki_tall.sort()
    yuki_max = yuki_tall[-1]

    for line in yuki_tall:
        search_num = kijun - line

        if search_num > yuki_max:
            yuki_num = yuki_num - 1
        else:
            index = np.searchsorted(yuki_tall,search_num)
            result = result + 1
            yuki_tall.pop(index)
            yuki_num = yuki_num -  2

        if yuki_num <= 1:
            if line >= kijun:
                result = result + 1
            break

        yuki_max = yuki_tall[-1]
    return result
a = yuki(1 , 1 , [0] , -1)
b = yuki(yuki_num , kijun , yuki_tall , 0)
print(b)
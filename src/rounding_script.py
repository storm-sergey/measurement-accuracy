from __future__ import annotations
from typing import Optional
import numpy as np


class SingletonMeta(type):
    _instance: Optional[Rnd] = None

    def __call__(self) -> Rnd:
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance


class Rnd(metaclass=SingletonMeta):
    __round_position = None

    @staticmethod
    def round_to_position(num, pos):
        return np.around(num, pos)

    @staticmethod
    def round_like_sig(num):
        if Rnd().__round_position is None:
            print('********************************************************')
            print('At first you have to round full error and relative error')
            print('********************************************************')
            raise AssertionError
        else:
            return np.around(num, Rnd().__round_position)

    @staticmethod
    def round_sig(num):
        if num < 0:
            return -Rnd().round_sig(abs(num))
        elif num == 0:
            return 0
        elif (num > 0) and (num < 1):
            for i, n in enumerate(str(num)[2:]):
                if n == '0':
                    pass
                elif n == '1':
                    Rnd().__round_position = i + 2
                    return np.around(num, Rnd().__round_position)
                else:
                    Rnd().__round_position = i + 1
                    return np.around(num, Rnd().__round_position)
        elif num == 1:
            Rnd().__round_position = 2
            return np.around(num, Rnd().__round_position)
        elif num > 1:
            if str(int(num))[-1] == '1':
                Rnd().__round_position = 1
                return np.around(num, Rnd().__round_position)
            Rnd().__round_position = 0
            return int(np.around(num))
        else:
            raise ValueError


def __print_test(n_list):
    for n in n_list:
        print(Rnd().round_sig(n), 'from', n)


def test():
    __print_test((-0,
                  1,
                  1.11111,
                  0.0001111,
                  0.01555,
                  0.000911,
                  9.11,
                  -112.112,
                  ))


if __name__ == '__main__':
    test()

from matplotlib import pyplot as plt
import numpy as np
from rounding_script import Rnd


class ObErrCalc:

    def express_solution(self):
        self._express_instrument_error(self._fig, 0.05, 0.90,
                                       self._title,
                                       self._instr_err)
        self._express_avg(self._fig, 0.05, 0.85,
                          self._title,
                          self._num_row,
                          self._average,
                          self._r_average)
        self._express_avg_num_deltas(self._fig, 0.05, 0.75,
                                     self._title,
                                     self._num_row,
                                     self._average,
                                     self._avg_num_deltas)
        self._express_random_error(self._fig, 0.05, 0.35,
                                   self._title,
                                   self._avg_num_deltas,
                                   self._random_error)
        self._express_full_error(self._fig, 0.05, 0.25,
                                 self._title,
                                 self._instr_err,
                                 self._full_error,
                                 self._random_error)
        self._express_relative_error(self._fig, 0.05, 0.20,
                                     self._title,
                                     self._average,
                                     self._full_error,
                                     self._relative_error)
        self._express_result(self._fig, 0.05, 0.15,
                             self._unit,
                             self._title,
                             self._r_average,
                             self._full_error,
                             self._relative_error)

    def __init__(self,
                 title: str,
                 measure_unit: str,
                 nums,
                 instrument_error: float,
                 size=(14.00, 6.50),
                 dpi=100,
                 rnd_pos=4, ):
        # TODO Refactor this block
        self._fig = plt.figure(figsize=size, dpi=dpi)
        self._unit = measure_unit
        self._title = title
        self._num_row = np.array(nums)
        self._instr_err = instrument_error
        self._average = Rnd().round_to_position(self._get_avg(self._num_row), rnd_pos)
        self._avg_num_deltas = Rnd().round_to_position(self._get_avg_num_deltas(self._num_row, self._average), rnd_pos)
        self._random_error = Rnd().round_to_position(self._get_random_error(self._avg_num_deltas), rnd_pos)
        self._full_error = Rnd().round_sig(self._get_full_error(instrument_error, self._random_error))
        self._relative_error = Rnd.round_sig(self._get_relative_error(self._average, self._full_error))
        self._r_average = Rnd().round_like_sig(self._average)

    def _get_avg(self, num_row):
        return np.average(num_row)

    def _get_avg_num_deltas(self, num_row, avg):
        return [avg - num for num in num_row]

    def _get_random_error(self, deltas):
        try:
            return np.sqrt(
                np.sum([delta ** 2 for delta in deltas]) / (
                        (len(deltas) ** 2) - len(deltas)))  # n(n-1)
        except ZeroDivisionError:
            print(ZeroDivisionError)
            return 0

    def _get_full_error(self, instrument_error, random_error):
        return instrument_error + random_error

    def _get_relative_error(self, avg, full_err):
        try:
            return full_err / avg
        except ZeroDivisionError:
            print(ZeroDivisionError)
            return 0

    def _express_instrument_error(self, fig, x, y, title, instr_err):
        # TODO express instr_err like int if it isn't a float
        fig.text(x, y, r'$\Delta{%s}_{instrument} = ' % title
                 + f'{instr_err}$')

    def _express_avg(self, fig, x, y, title, num_row, avg, r_avg):
        sym_sum = f'{title}_{1}'
        for n in range(1, len(num_row)):
            sym_sum += r' + {%s}_{%s}' % (title, n + 1)
        num_sum = f'{num_row[0]}'
        for num in num_row[1:]:
            num_sum += r' + {%s}' % num
        sym_avg = r'\frac{%s}{%s}' % (sym_sum, len(num_row))
        num_avg = r'\frac{%s}{%s}' % (num_sum, len(num_row))
        fig.text(x, y, r'$\overline{%s} = ' % title
                 + f'{sym_avg} = $')
        fig.text(x + 0.004, y - 0.05,
                 f'$ = {num_avg} = '
                 + f'{str(avg)} = '
                 + str(r_avg)
                 + '$')

    def _express_avg_num_deltas(self, fig, x, y, title, num_row, avg, deltas):
        for i, delta in enumerate(deltas):
            n = i + 1
            fig.text(x + ((i // 10) / 4),
                     # 'x' shifts to right by 1/4 of canvas when 10 deltas is already shown
                     y - (i / 30) + ((i // 10) / 3),
                     # 'y' shifts to down by 1/30 canvas and raises back when 10 row is shown
                     r'$\Delta_{%s} = ' % n
                     + r'\overline{%s} - ' % title
                     + r'{%s}_{%s} = ' % (title, n)
                     + f'{avg} - {num_row[i]} = '
                     + f'{delta}$')

    def _express_random_error(self, fig, x, y, title, deltas, rand_err):
        delta_symbols_sum = r'\Delta_{1}^2'
        deltas_sum = r''
        if deltas[0] >= 0:
            deltas_sum = f'{deltas[0]}^2'
        elif deltas[0] < 0:
            deltas_sum = f'({deltas[0]})^2'
        for i, delta in enumerate(deltas[1:]):
            n = i + 1
            delta_symbols_sum += r' + \Delta_{%s}^2' % n
            if delta >= 0:
                deltas_sum += ' + {%s}^2' % delta
            elif delta < 0:
                deltas_sum += ' + ({%s})^2' % delta
        fig.text(x, y, r'$\Delta\overline{%s}_{random} = ' % title
                 + r'\sqrt{\frac{%s}{%s}} = $' % (delta_symbols_sum, 'n(n-1)'))
        fig.text(x + 0.038, y - 0.05,
                 r'$ = \sqrt{\frac{%s}{%s}} = ' % (deltas_sum, (f'{len(deltas)}' + r'\cdot' + f'{len(deltas) - 1}'))
                 + f'{rand_err}$')

    def _express_full_error(self, fig, x, y, title, instrument_error, full_error, rand_err):
        fig.text(x, y, r'$\Delta{%s}_{full} = ' % title
                 + r'\Delta\overline{%s}_{random} +' % title
                 + r'\Delta{%s}_{instrument} = ' % title
                 + f'{rand_err} + {instrument_error} = '
                 + f'{rand_err+instrument_error} = '
                 + f'{full_error}$')

    def _express_relative_error(self, fig, x, y, title, avg, full_err, relative_error):
        fig.text(x, y, r'$\epsilon({%s}) = ' % title
                 + r'\frac{\Delta{%s}_{full}}{\overline{%s}} = ' % (title, title)
                 + r'\frac{%s}{%s} = ' % (full_err, avg)
                 + f'{relative_error}$')

    def _express_result(self, fig, x, y, unit, title, avg, full_err, rel_err):
        fig.text(x, y, r'$Final\ result:\ '
                 + f'{title} = '
                 + r'(\overline{%s}\pm\Delta{%s}_{full}) = ' % (title, title)
                 + r'({%s}\pm{%s})\ {%s};$' % (avg, full_err, unit))
        fig.text(x, y - 0.03, '                     '
                 + r'$\epsilon({%s}) = {%s}$' % (title, rel_err))


def test():
    row = [12, 9, 11, 9, 9.5, 10, 13, 11.5, 10.5, 11, 9.5, 10.5, 11,
           12, 9, 11, 9, 9.5, 10, 13, 11.5, 10.5, 11, 9.5, 10.5, 11, ]
    ObErrCalc(measure_unit='sec', title='t', nums=row[14:], instrument_error=0.2).express_solution()
    plt.show()


if __name__ == '__main__':
    test()

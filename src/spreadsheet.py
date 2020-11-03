from __future__ import annotations
import pandas as pd
from typing import Optional


class SingletonMeta(type):
    _instance: Optional[Spreadsheet] = None

    def __call__(self) -> Spreadsheet:
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance


class Spreadsheet(metaclass=SingletonMeta):

    def columns(self):
        return self._formatted_data

    class Column:

        def get_title(self):
            return self.title

        def get_instr_err(self):
            return self.instrument_error

        def get_unit(self):
            return self.measure_unit

        def get_nums(self):
            return self.nums

        def get_all(self):
            return (self.title,
                    self.instrument_error,
                    self.measure_unit,
                    self.nums, )

        def __init__(self, *nums: float, title: str, instr_err: float, unit: str):
            self.title = title
            self.instrument_error = instr_err
            self.measure_unit = unit
            self.nums = [*nums]

    def __init__(self, file_name: str = './Measurements.xls', ):
        try:
            try:
                self._formatted_data = self._get_formatted_data(self._get_raw_dict(file_name))
            except (FileNotFoundError, FileNotFoundError):
                self._formatted_data = self._get_formatted_data(self._get_raw_dict(file_name + 'x'))
        except (FileNotFoundError, FileExistsError):
            print('File \"' + file_name + '\" not found')
            exit(0)

    def _get_raw_dict(self, file_name):
        return pd.read_excel(file_name, keep_default_na=False, index_col=None, header=0).to_dict()

    def _get_formatted_data(self, raw_dict):
        columns_list = list()
        for column in raw_dict.keys():
            raw_values = [val for val in raw_dict.get(column).values() if val != ''][2:]
            columns_list.append(self.Column(
                *[float(val) for val in raw_values],
                title=str(column),
                instr_err=float(raw_dict[column][0]),
                unit=str(raw_dict[column][1])))
        return columns_list


def test():
    spreadsheet = Spreadsheet().columns()
    for column in spreadsheet:
        print(column.get_all())


if __name__ == '__main__':
    test()

from solution_template import TTest
from spreadsheet import Spreadsheet
from matplotlib import pyplot as plt
from matplotlib import backend_bases


def show_all():
    # TODO make toolbar buttons work
    ntb = backend_bases.NavigationToolbar2
    ntb.toolitems = (
        ('Home', 'Reset original view', 'home', 'home'),
        (None, None, None, None),
        ('Back', 'Back to  previous view', 'back', 'back'),
        ('Forward', 'Forward to next view', 'forward', 'forward'),
        (None, None, None, None),
        ('Save', 'Save the figure', 'filesave', 'save_figure'),)
    for column in Spreadsheet().columns():
        TTest(title=column.get_title(),
              measure_unit=column.get_unit(),
              instrument_error=column.get_instr_err(),
              nums=column.get_nums(),
              dpi=130,
              ).express_solution()
    plt.show()


def test():
    row = [12, 9, 11, 9, 9.5, 10, 13, 11.5, 10.5, 11, 9.5, 10.5, 11,
           12, 9, 11, 9, 9.5, 10, 13, 11.5, 10.5, 11, 9.5, 10.5, 11, ]
    TTest(measure_unit='sec', title='t', nums=row[14:], instrument_error=0.2).express_solution()
    TTest(measure_unit='sec', title='t', nums=row[:12], instrument_error=0.2).express_solution()
    plt.show()


if __name__ == '__main__':
    #  test()
    show_all()

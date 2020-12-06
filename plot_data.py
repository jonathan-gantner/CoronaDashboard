"""
Creates plots for Covid19 AGES data.
"""

import datetime as dt
import pandas as pd
from typing import Union, List, Optional

import load_data as ld
from matplotlib import pyplot as plt

def plot_deltas(data: pd.DataFrame, kinds: Union[str, List[str]], ylog: Optional[bool] = True,
                start: Optional[dt.date] = None, end: Optional[dt.date] = dt.date.today()):
    """
    Plots the deltas

    :param data:
    :param kinds:
    :param ylog:
    :param start:
    :param end:
    :return:
    """
    pass


def plot_icus_time_line(regions: Union[str, List[str]] = 'Alle',
                        start: Optional[dt.date] = ld.FIRST_DAY_OF_HISTORIES,
                        end: Optional[dt.date] = dt.date.today(),
                        data: Optional[pd.DataFrame] = None):
    if data is None:
        data = ld.load_ages_capacity_data(start, end)
    else:
        data = data.loc[start < data['date'] < end, :]

    if isinstance(regions, str):
        regions = [regions]

    # fig, ax = plt.figure()
    legend_labels = []
    for reg in regions:
        region_data = data.loc[data['region'] == reg, :]
        region_data.plot(x='date', y='icu')
        plt.plot(region_data['date'], region_data['icu'] + region_data['icu_free'])
        legend_labels.extend([f'ICU {reg}', f'Total ICU {reg}'])

    plt.xlabel('Time')
    plt.ylabel('ICU Units')
    plt.legend(legend_labels)
    plt.show()


if __name__=='__main__':
    plot_icus_time_line()
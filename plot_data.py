"""
Creates plots for Covid19 AGES data.
"""

import datetime as dt
import pandas as pd
from typing import Union, List, Optional

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
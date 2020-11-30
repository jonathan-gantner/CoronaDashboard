import requests
import config
import zipfile
import io
import datetime as dt
import os
import pandas as pd
from typing import Optional, List, Union


def download_ages_data(destination: Optional[str]=config.ages_dir):
    """
    Downloads data
    :param destination: destination directory
    :return:
    """
    r = requests.get(config.ages_url, stream=True)
    zf = zipfile.ZipFile(io.BytesIO(r.content))
    zf.extractall(destination)


def load_ages_deltas(start: dt.date, end: dt.date,
                     file: str = os.path.join(config.ages_dir, 'CovidFaelleDelta.csv')) -> pd.DataFrame:
    """
    Loads the time series of deltas w.r.t. the previous days for all of Austria from the AGES file CovidFaelleDelta.csv.

    :param file: ages file
    :param start:
    :param end:
    :param kinds:
    :return: pd.DataFrame with columns 'date', 'infected', 'recovered', 'died', 'active', and 'tested'
    """

    rename_map = {
        'Datum': 'date',
        'DeltaAnzahlVortag': 'infected',
        'DeltaGeheiltVortag': 'recovered',
        'DeltaTotVortag': 'died',
        'DeltaAktivVortag': 'active',
        'DeltaTestGesamtVortag': 'tested'
    }
    data = pd.read_csv(file, header=0, sep=';').rename(columns=rename_map)
    data['date'] = pd.to_datetime(data['date'], format='%d.%m.%Y %H:%M:%S')

    data = data.loc[(data['date'].dt.date < end ) & (data['date'].dt.date > start)]

    return data


def load_ages_capacity_data(start: dt.date, end: dt.date,
                    file: str = os.path.join(config.ages_dir, 'CovidFallzahlen.csv')) -> pd.DataFrame:
    """
    Loads the time series of available and used capacity in Austria from the AGES file CovidFallzahlen.csv.

    :param start:
    :param end:
    :param file:
    :return: pd.DataFrame with columns 'date', 'tested', 'date', 'hospitalized', 'icu', 'hospital_free', 'icu_free',
        'region'
    """
    # ToDo: MultiIndex Date + Region?
    rename_map = {
        'TestGesamt': 'tested',
        'MeldeDatum': 'date',
        'FZHosp': 'hospitalized',
        'FZICO': 'icu', # intensive care unit
        'FZHospFree': 'hospital_free',
        'FZICUFree': 'icu_free',
        'BundeslandID': 'region_id',
        'Bundesland': 'region'
    }
    columns_to_drop = ['Meldedat']

    data = pd.read_csv(file, header=0, sep=';').rename(columns=rename_map).drop(columns=columns_to_drop)
    data['date'] = pd.to_datetime(data['date'], format='%d.%m.%Y %H:%M:%S')

    data = data.loc[(data['date'].dt.date < end ) & (data['date'].dt.date > start)]

    return data


if __name__ == '__main__':
    # download_ages_data()
    # start = dt.date(day=1, month=7, year=2020)
    end = dt.date.today()
    start = end - dt.timedelta(days=20)

    data_deltas = load_ages_deltas(start, end)
    print(data_deltas)

    data_hosp = load_ages_capacity_data(start, end)
    print(data_hosp)
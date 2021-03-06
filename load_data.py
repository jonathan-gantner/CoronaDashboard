import requests
import config
import zipfile
import io
import datetime as dt
import os
import pandas as pd
from typing import Optional, List, Union

FIRST_DAY_OF_HISTORIES = dt.date(year=2020, month=2, day=26)


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
        'FZICU': 'icu', # intensive care unit
        'FZHospFree': 'hospital_free',
        'FZICUFree': 'icu_free',
        'BundeslandID': 'region_id',
        'Bundesland': 'region'
    }
    columns_to_drop = ['Meldedat']

    data = pd.read_csv(file, header=0, sep=';').rename(columns=rename_map).drop(columns=columns_to_drop)
    data['date'] = pd.to_datetime(data['date'], format='%d.%m.%Y %H:%M:%S')

    data = data.loc[(data['date'].dt.date < end) & (data['date'].dt.date > start)]

    return data


def load_ages_cases_by_age_and_sex(file: str = os.path.join(config.ages_dir, 'CovidFaelle_Altersgruppe.csv')
                                   ) -> pd.DataFrame:
    """
    Loads the current numbers of total infected, recovered and died cases in Austria by age group and sex
    from the AGES file CovidFallzahlen.csv.

    :param file:
    :return: pd.DataFrame with columns 'age_group_id', 'age_group', 'region', 'region_id', 'population', 'sex',
        'total', 'recovered', and 'dead'
    """

    # ToDo: MultiIndex Date + Region?
    rename_map = {
        'AltersgruppeID': 'age_group_id',
        'Altersgruppe': 'age_group',
        'Bundesland': 'region',
        'BundeslandID': 'region_id',
        'AnzEinwohner': 'population',
        'Geschlecht': 'sex',
        'Anzahl': 'total',
        'AnzahlGeheilt': 'recovered',
        'AnzahlTot': 'dead'
    }

    data = pd.read_csv(file, header=0, sep=';').rename(columns=rename_map)
    return data


def load_ages_cases_by_district(file: str = os.path.join(config.ages_dir, 'CovidFaelle_GKZ.csv')
                                 ) -> pd.DataFrame:
    """
    Loads the current numbers of total active, recovered and died cases by district in Austria from the AGES file
    CovidFaelle_GKZ.csv.

    :param file:
    :return: pd.DataFrame with columns 'district', 'district_id', 'population', 'total', 'dead', 'cases_7days'
    """
    # ToDo: MultiIndex Date + Region?
    rename_map = {
        'Bezirk': 'district',
        'GKZ': 'district_id',
        'AnzEinwohner': 'population',
        'Anzahl': 'total',
        'AnzahlTot': 'dead',
        'AnzahlFaelle7Tage': 'cases_7days'
    }

    data = pd.read_csv(file, header=0, sep=';').rename(columns=rename_map)
    return data


def load_ages_cases_by_district_series(start: dt.date, end: dt.date,
                                        file: str = os.path.join(config.ages_dir, 'CovidFaelle_Timeline_GKZ.csv')
                                        ) -> pd.DataFrame:
    """
    Loads the time series of cases per district from the file  CovidFaelle_Timeline_GKZ.csv.

    :param file: ages file
    :param start:
    :param end:
    :param kinds:
    :return: pd.DataFrame with columns 'date', 'district', 'district_id', 'population', 'infected', 'total',
        'cases_7days', '7days_incidence', 'dead', 'dead_total', 'recovered', 'recovered_total'
    """

    rename_map = {
        'Time': 'date',
        'Bezirk': 'district',
        'GKZ': 'district_id',
        'AnzEinwohner': 'population',
        'AnzahlFaelle': 'infected',
        'AnzahlFaelleSum': 'total',
        'AnzahlFaelle7Tage': 'cases_7days',
        'SiebenTageInzidenzFaelle': '7days_incidence',
        'AnzahlTotTaeglich': 'dead',
        'AnzahlTotSum': 'dead_total',
        'AnzahlGeheiltTaeglich': 'recovered',
        'AnazhlGeheiltSum': 'recovered_total'
    }
    data = pd.read_csv(file, header=0, sep=';').rename(columns=rename_map)
    data['date'] = pd.to_datetime(data['date'], format='%d.%m.%Y %H:%M:%S')
    data = data.loc[(data['date'].dt.date < end) & (data['date'].dt.date > start)]

    return data


def load_ages_cases_timeline(start: dt.date, end: dt.date,
                             file: str = os.path.join(config.ages_dir, 'CovidFaelle_Timeline.csv')) -> pd.DataFrame:
    """
    Loads the time series of Covid cases from the file CovidFaelle_Timeline.csv.

    :param file: ages file
    :param start:
    :param end:
    :param kinds:
    :return: pd.DataFrame with columns 'date', 'infected', 'recovered', 'died', 'active', and 'tested'
    """

    rename_map = {
        'Time': 'date',
        'Bundesland': 'region',
        'BundeslandID': 'region_id',
        'AnzEinwohner': 'population',
        'AnzahlFaelle': 'infected',
        'AnzahlFaelleSum': 'total',
        'AnzahlFaelle7Tage': 'cases_7days',
        'SiebenTageInzidenzFaelle': '7days_incidence',
        'AnzahlTotTaeglich': 'dead',
        'AnzahlTotSum': 'dead_total',
        'AnzahlGeheiltTaeglich': 'recovered',
        'AnazhlGeheiltSum': 'recovered_total'
    }
    data = pd.read_csv(file, header=0, sep=';', decimal=',').rename(columns=rename_map)
    data['date'] = pd.to_datetime(data['date'], format='%d.%m.%Y %H:%M:%S')


    data = data.loc[(data['date'].dt.date < end) & (data['date'].dt.date > start)]

    return data


#ToDo: data validation checks


if __name__ == '__main__':
    # download_ages_data()
    # start = dt.date(day=1, month=7, year=2020)
    end = dt.date.today()
    start = end - dt.timedelta(days=20)

    data_deltas = load_ages_deltas(start, end)
    print(data_deltas)

    data_hosp = load_ages_capacity_data(start, end)
    print(data_hosp)

    cases_age_and_sex = load_ages_cases_by_age_and_sex()
    print(cases_age_and_sex)

    cases_district = load_ages_cases_by_district()
    print(cases_district)

    cases_district_series = load_ages_cases_by_district_series(start=start, end=end)
    print(cases_district_series)

    cases_timeline = load_ages_cases_timeline(start, end)
    print(cases_timeline)



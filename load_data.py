import requests
import config
import zipfile
import io

from typing import Optional


def load_ages_data(destination: Optional[str]=config.ages_dir):
    """
    Downloads data
    :param destination: destination directory
    :return:
    """
    r = requests.get(config.ages_url, stream=True)
    zf = zipfile.ZipFile(io.BytesIO(r.content))
    zf.extractall(destination)


if __name__ == '__main__':
    load_ages_data()
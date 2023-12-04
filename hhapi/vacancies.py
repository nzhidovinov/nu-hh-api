import time
import requests
from functools import partial


def search_vacancies(query: str, page: int = 0, per_page: int = 10,
                     sleep: float = 0.1, base_url: str = 'https://api.hh.ru/vacancies'):
    kwargs = locals().copy()
    kwargs.update(page=page + 1)
    next_page = partial(search_vacancies, **kwargs)

    params = {
        'text': query,
        'per_page': per_page,
        'page': page
    }

    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        return

    vacancies = response.json()['items']
    for vacancy in vacancies:
        vacancy_data = requests.get(vacancy['url']).json()
        yield vacancy_data

    time.sleep(sleep)
    yield from next_page()

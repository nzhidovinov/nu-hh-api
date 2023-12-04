import json
import argparse
from tqdm import tqdm
from pprint import pprint
from collections import Counter
from hhapi.vacancies import search_vacancies


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('query',
                        help='Search query')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()

    filters = (
        lambda x: not x.get('archived', False),  # not archived
        lambda x: x.get('key_skills', False),    # key_skills not empty
    )

    skills = []
    for vacancy in tqdm(search_vacancies(args.query)):
        if all(f(vacancy) for f in filters):
            skills.extend(skill['name'].lower() for skill in vacancy['key_skills'])

    statistics = Counter(skills)
    with open(f'{args.query}.json', 'w') as f:
        json.dump(statistics, f, ensure_ascii=False, indent=4)
    pprint(statistics.most_common(10))

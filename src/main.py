import asyncio
import re
from typing import List

from bs4 import BeautifulSoup, Tag
from httpx import AsyncClient, Response

from bot.handlers.notifications import send_notification
from sql import is_checked, set_check
from utils import normalize_query


async def get_latest_vacancies(query: str = '') -> Response:
    normalized_query = normalize_query(query)

    async with AsyncClient() as client:
        response = await client.get(
            'https://hh.ru/search/vacancy?'
            'search_field=name'
            '&search_field=company_name'
            '&search_field=description'
            '&text=%s'
            '&ored_clusters=true'
            '&order_by=publication_time' % normalized_query,
        )
        if response.status_code == 302:
            response = await client.get(response.headers.get('location'))
        return response


async def get_vacancy_description(href: str) -> Tag:
    async with AsyncClient() as client:
        response = await client.get(href)
    soup = BeautifulSoup(response, 'html.parser')
    soup = soup.find('div', class_='vacancy-section')
    soup = soup.select_one('div[data-qa]')
    return soup


def check_regular_conditions(bold_titles: List[Tag]) -> bool:
    """IF NOT FOUND AT LEAST ONE POINT IN THE END => return False"""
    found_at_least_one_point = False

    texts = list(map(lambda x: x.text.lower(), bold_titles))
    for text in texts:
        if re.search(
            r'требов|от\s*(вас|тебя)|ожида|жд[её]м|нужн|важн|навык|надоб|кандидат|ищем|необходим',
            text,
        ):
            found_at_least_one_point = True
            """ GET LIST OF CONDITION """
            ul = bold_titles[texts.index(text)].find_parent('p').find_next_sibling()
            li_tags = ul.find_all('li')

            for li in li_tags:
                bigger_than = r'(больше|от|>|=>|>=)'
                at_least = r'(не\s*менее|минимум|не\s*меньше|от)'
                conditions = (
                    rf'(.*({bigger_than}|{at_least}).*(года|лет).*.*опыт.*)',
                    rf'(.*опыт.*({bigger_than}|{at_least}).*(года|лет).*)',
                    rf'(.*python.*({bigger_than}|{at_least}).*(года|лет).*)',
                )
                if re.search(
                    r'|'.join(conditions),
                    li.text.lower(),
                ):
                    return False

    if found_at_least_one_point:
        return True
    return False


async def create_task(link: Tag) -> None:
    href = link.get('href')

    if not is_checked(href):
        description = await get_vacancy_description(href)
        bold_titles = description.select('p > strong')

        if check_regular_conditions(bold_titles):
            set_check(href)
            await send_notification(href)


async def create_tasks(links: List[Tag]) -> List[asyncio.Task]:
    tasks = []
    for link in links:
        tasks.append(
            asyncio.create_task(
                create_task(link),
            ),
        )
    return tasks


async def get_vacancy_list(query: str = '') -> List[Tag]:
    response = await get_latest_vacancies(query)
    vacancies = BeautifulSoup(response, 'html.parser')
    links = vacancies.find_all('a', class_='serp-item__title')
    return links


async def main():
    links = await get_vacancy_list('Python fastapi')
    tasks = await create_tasks(links)
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())

import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import json


def get_headers():
    return Headers(browser='opera', os='win').generate()


url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
words = {
    'text': 'python django flask',
    'items_on_page': 20,
    'page': 0
}
print(f'Ищем подходящие вакансии')
job_data = []
try:
    while True:
        job_html = requests.get(url=url, params=words, headers=get_headers()).text
        job_soup = BeautifulSoup(job_html, 'lxml')
        words['page'] += 1
        main_content = job_soup.find('div', id='a11y-main-content')
        div_item_tags = main_content.find_all('div', class_='serp-item')


        for div_item_tag in div_item_tags:
            vacancy = div_item_tag.find('h3')
            link = vacancy.find('a').get('href')
            try:
                salary = div_item_tag.find('span', class_='bloko-header-section-3').text.replace('\u202f', '')
            except:
                salary = 'Не указана'
            company = div_item_tag.find('a', class_='bloko-link bloko-link_kind-tertiary').text.replace('\xa0', '')
            city = div_item_tag.find('div', class_='vacancy-serp-item__info').contents[1].contents[0]
            job_data.append(
                {
                    "Город": city,
                    "Компания": company,
                    "Вакансия": vacancy.text,
                    "Зарплата": salary,
                    "Ссылка": link,
                }
            )

except:
    print(f'Найдено {len(job_data)} вакансий')

if __name__ == "__main__":
    with open('jobs.json', 'w', encoding='utf-8') as f:
        json.dump(job_data, f, ensure_ascii=False, indent=5)
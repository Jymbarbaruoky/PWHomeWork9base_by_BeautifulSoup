import json
from typing import List, Dict

import requests
from bs4 import BeautifulSoup


base_url = 'http://quotes.toscrape.com'
pages_urls = [base_url, ]
authors_urls = []


def get_pages_urls(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    page_url = soup.select('li[class="next"] a')
    if page_url:
        pages_urls.append(f'{base_url}{page_url[0]["href"][:-1]}')
        return get_pages_urls(f'{base_url}{page_url[0]["href"][:-1]}')


def get_authors_urls():
    suffix_authors_urls = []
    for page_url in pages_urls:
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        authors_in_page = soup.select('div[class=quote] span a')
        for autor_url in authors_in_page:
            if f'{autor_url["href"]}' not in suffix_authors_urls:
                suffix_authors_urls.append(f'{autor_url["href"]}')
                authors_urls.append(f'{base_url}{autor_url["href"]}')


def get_quotes_in_page(url) -> List:
    data = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('span', class_='text')
    authors = soup.find_all('small', class_='author')
    tags_lists = soup.find_all('div', class_='tags')

    for i in range(0, len(quotes)):
        tagsforquote = tags_lists[i].find_all('a', class_='tag')
        tags = []
        for tagforquote in tagsforquote:
            tags.append(tagforquote.text)
        data.append({
            'tags': tags,
            'author': authors[i].text,
            'quote': quotes[i].text
        })
    return data


def get_author(url) -> Dict:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    fullname = soup.find('h3', class_='author-title')
    born_date = soup.find('span', class_='author-born-date')
    born_location = soup.find('span', class_='author-born-location')
    description = soup.find('div', class_='author-description')

    result = {
            'fullname': fullname.text.replace('\n', '').strip(),
            'born_date': born_date.text,
            'born_location': born_location.text,
            'description': description.text[2:].strip()
             }
    return result


def write_authors_to_json():
    data = []
    for url in authors_urls:
        data.append(get_author(url))
    with open('data/authors.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


def write_quotes_to_json():
    data = []
    for url in pages_urls:
        data.extend(get_quotes_in_page(url))
    with open('data/quotes.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


def main():
    get_pages_urls(base_url)
    get_authors_urls()
    write_authors_to_json()
    write_quotes_to_json()


if __name__ == '__main__':
    main()

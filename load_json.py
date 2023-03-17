from models import Authors, Quotes
import json


def create_autor(path: str):
    with open(path, encoding='utf-8') as f:
        authors = json.load(f)
    for autor in authors:
        Authors(fullname=autor.get('fullname'), born_date=autor.get('born_date'),
                born_location=autor.get('born_location'), description=autor.get('description')).save()


def create_quote(path: str):
    with open(path, encoding='utf-8') as f:
        quotes = json.load(f)
    for quote in quotes:
        autor = Authors.objects(fullname=quote.get('author'))
        for a in autor:
            Quotes(tags=quote.get('tags'), author=a.id, quote=quote.get('quote')).save()


def create():
    create_autor('data/authors.json')
    create_quote('data/quotes.json')


if __name__ == '__main__':
    create()

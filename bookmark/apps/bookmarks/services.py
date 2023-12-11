import re

from bs4 import BeautifulSoup
import requests


class OpenGraphParse:
    """
    Получение страницы и парсинг OpenGraph атрибутов
    """

    _required_attrs = ('title', 'type', 'image', 'url', 'description')

    def __init__(self, url):
        self._parsed_attrs = dict()
        self._url = url
        self.parse_page()

    def get_page(self):
        try:
            response = requests.get(self._url)
        except requests.exceptions.RequestException:
            raise self.PageRetrieveException()
        return response.content

    def parse_page(self):
        soup = BeautifulSoup(self.get_page(), 'lxml')
        tags = soup.html.head.findAll(property=re.compile(r'^og'))

        for tag in tags:
            if (
                    tag.has_attr(u'content') and
                    tag[u'property'][3:] in self._required_attrs
            ):
                value = tag[u'content'].split('.')[0]
                self._parsed_attrs[tag[u'property'][3:]] = value

        for attr in self._required_attrs:
            if attr not in self._parsed_attrs.keys():
                match attr:
                    case u'title':
                        self._parsed_attrs['title'] = self.alter_title(soup)
                    case u'description':
                        description = self.alter_description(soup)
                        self._parsed_attrs['description'] = description
                    case u'url':
                        self._parsed_attrs['url'] = self._url

    def alter_title(self, soup):
        title = soup.html.head.title
        if title:
            return title.text
        return 'No title'

    def alter_description(self, doc):
        tag = doc.html.head.findAll('meta', attrs={'name': 'description'})
        result = ''.join([t['content'] for t in tag])
        return result if result else 'no description'

    @property
    def get_data(self):
        return self._parsed_attrs

    class PageRetrieveException(Exception):
        pass

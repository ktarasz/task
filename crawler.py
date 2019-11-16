from random import randint
import requests
from lxml import html
from urllib.parse import urlparse


BASE_URL = 'https://github.com'
SEARCH_URL = f'{BASE_URL}/search'

TYPE_MAPPER = {
    'Repositories': '//li[contains(@class, \'repo-list-item\')]//h3/a',
    'Issues': '//div[@class and contains(@class, \'issue-list-item\')]//h3/a',
    'Wikis': '//div[@class and contains(@class, \'wiki-list-item\')]/div/div/a[2]'
}

PAGE_SIZE = 10


class GithubWebSearch:
    """
    GitHub Web Search Crawler
    """


    def __init__(self, keywords=(), object_type='Repositories', extra=True, proxies=()):
        """
        :param keywords: list of words for search query
        :type keywords: list, tuple
        :param proxies: list of proxies used for make requests
        :type proxies: list, tuple
        :param object_type: types of information for search
        :type object_type: str
        """
        self.keywords = ' '.join(keywords)
        self.proxies = list([
            f'https://{proxy}'
            for proxy in proxies
        ])
        self.object_type = object_type
        self.extra = extra
        self.page = 1

    def get_proxy_for_request(self):
        """
        :return: random proxy dict for requests proxy keyword argument
        """
        if self.proxies:
            proxy_index = randint(0, len(self.proxies) - 1)
            return {'https': self.proxies[proxy_index]}

    def make_search(self):
        """

        :param page:
        :type page: int
        :return:
        """
        params = {'p': self.page, 'q': self.keywords, 'type': self.object_type}
        return self._request(SEARCH_URL, params)

    def _request(self, url, params={}):
        r = requests.get(url, params=params,
                          proxies=self.get_proxy_for_request(),
                          stream=True)
        r.raise_for_status()
        return html.fromstring(r.content)


    def __iter__(self):
        """
        :return: return list of dicts for crawler results
        """
        while 1:
            data = self.get_data(self.make_search())
            if self.extra and self.object_type == 'Repositories':
                data = list(map(self.get_repo_extra, data))
            yield data
            if len(data) < 10:
                break
            self.page += 1

    def get_data(self, tree):
        """
        :param tree: lxml.Element for parse
        :type tree: lxml.Element
        :return: base information about searched item
        """
        return [
            {'url': f'{BASE_URL}{el.attrib["href"]}'}
            for el in tree.xpath(TYPE_MAPPER.get(self.object_type))
        ]

    def get_repo_extra(self, item):
        """
        :param item: repository collected data item
        :return: repository collected data item with extra
        """
        item['extra'] = {'owner': urlparse(item['url']).path.split('/')[1]}

        html_element = self._request(item['url'])
        lang_stats_elements = html_element.xpath(
            '//div[@class and contains(@class, \'repository-lang-stats-graph\')]/span'
        )
        if lang_stats_elements:
            item['extra']['language_stats'] = {}
            for lang_element in lang_stats_elements:
                lang_value_list = lang_element.attrib['aria-label'].split()
                lang_value = lang_value_list.pop(-1)
                lang_value = float(lang_value.rstrip('%'))
                item['extra']['language_stats'][' '.join(lang_value_list)] = lang_value

        return item


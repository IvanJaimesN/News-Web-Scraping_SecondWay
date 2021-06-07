from requests.models import parse_header_links
import bs4
import requests

from common import config

class NewsPage: ## Contiene el código auxiliar
    
    def __init__(self, news_site_uid, url):
        self._config = config()['news_sites'][news_site_uid]
        self._queries = self._config['queries']
        self._html = None
        self._url = url

        self._visit(url)

    def _select(self, query_string):
        return self._html.select(query_string)

    def _visit(self, url):
        response = requests.get(url)

        response.raise_for_status() ## entrega el estado

        self._html = bs4.BeautifulSoup(response.text, 'html.parser')        


class HomePage(NewsPage): ## HomePage (hijo) contiene a NewsPage y
                          ## HomePage contiene una propiedad adicionall
    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url)

    @property
    def article_links(self):
        link_list = []
        for link in self._select(self._queries['homepage_article_links']):
            if link and link.has_attr('href'):
                link_list.append(link)
                print('LINK: ', link)   ################################################################################

        return set(link['href'] for link in link_list)


class ArticlePage(NewsPage):  ## ArticlePage extiende a NewsPage,
                              ## es decir es un tipo de página de noticias
    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url)

    ## Acceder al cuerpo y título de la noticia:
    @property
    def body(self):
        result = self._select(self._queries['article_body'])
        return result[0].text if len(result) else ''

    @property
    def title(self):
        result = self._select(self._queries['article_title'])
        return result[0].text if len(result) else ''
    @property
    def url(self):
        return self._url
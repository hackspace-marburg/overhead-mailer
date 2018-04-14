from bs4 import BeautifulSoup
from http.client import HTTPSConnection


class PmWikiOverheadGrepper:
    ''' A class to fetch topics from an Overhead in the hsmr's PmWiki
        
        wiki = PmWikiOverheadGrepper('hsmr.cc')
        print(wiki.get_overhead_topics('2017-09-11'))
    '''

    def __init__(self, domain):
        self._domain = domain

    def _download_page(self, page):
        ''' Downloads GET of page on self._domain and returns a tuple of
            HTTP status code and text or error if status code != 200.

            page: Full ressource, must start with /
        '''
        ret_tuple = (500, None)

        try:
            conn = HTTPSConnection(self._domain)
            conn.request('GET', page)

            resp = conn.getresponse()
            if resp.status == 200:
                ret_tuple = (200, resp.read())
            else:
                ret_tuple = (resp.status, resp.reason)

            conn.close()
        except:
            pass

        return ret_tuple

    def _reduce_wikitext(self, html):
        ''' Extracts the 'wikitext' section of a HTML page.
            
            html: HTML page as string
        '''
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.find_all('div', id='wikitext')

        if not text:
            return None
        # The topic list is always the first list
        return self._html_list_to_list(text[0].ul)

    def _html_list_to_list(self, ele):
        ''' Walk recursively over an UL which may contain LIs with other ULs
            and create a list of entries as string or tuple of text and list
            of the sublist.

            ele: BeautifulSoup's UL
        '''
        if len(ele) == 0:
            return []

        li = ele.li.extract()

        children = li.findChildren('ul')
        if children:
            children[0].extract()
            return [(li.text.strip(), self._html_list_to_list(children[0]))] + \
              self._html_list_to_list(ele)

        return [li.text.strip()] + self._html_list_to_list(ele)

    def get_overhead_topics(self, date):
        ''' Tries to fetch the given Overhead-page and returns a list of
            topics listed in the "Themen" list. The list may contain strings
            or tuples of strings and another list for nested topic lists.

            date: The Overhead's date as a string, format: YYYY-MM-DD
        '''
        (code, response) = self._download_page('/Overhead/' + date)

        if code != 200:
            raise ValueError(
              'The webserver returned a non-200 status code\nCode: {}\n{}'.
              format(code, response))

        return self._reduce_wikitext(response)

    @staticmethod
    def nested_list_to_str(lst, depth=0):
        ''' Formates a recursive list of string or tuples of string and list
            to a Markdown-like textual representation.

            lst: Input list
            depth: Recursion depth (defaults to 0)
        '''
        if not lst:
            return ''

        head, *tail = lst
        if type(head) == tuple:
            return (' ' * depth) + '- ' + head[0] + '\n' + \
              PmWikiOverheadGrepper.nested_list_to_str(head[1], depth + 2) + \
              PmWikiOverheadGrepper.nested_list_to_str(tail, depth)
        else:
            return (' ' * depth) + '- ' + head + '\n' + \
              PmWikiOverheadGrepper.nested_list_to_str(tail, depth)

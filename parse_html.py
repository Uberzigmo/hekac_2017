from lxml import html
from collections import defaultdict
import requests
import json

def from_html_to_csv(url):

    requests_session = requests.session()
    page = requests_session.get(url)

    html_tree = html.fromstring(page.content)

    if 'www.fio.cz' in url:

        structure = ('date', 'amount', 'type', 'name', 'messege', 'KS', 'VS', 'SS', 'note')

        transactions = defaultdict(lambda: {'date': '',
                                            'amount': '',
                                            'type': '',
                                            'name': '',
                                            'messege': '',
                                            'KS': '',
                                            'VS': '',
                                            'SS': '',
                                            'note': ''
                                            })

        # //table/tbody/tr/td[1]/text()

        for tr in enumerate(html_tree.xpath('//table/tbody/tr')[1:]):
            transactions[tr[0]]['date'] = tr[1].xpath('td[1]/text()'))


        return

print(from_html_to_csv('https://www.fio.cz/ib2/transparent?a=2600088789'))
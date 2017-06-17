from lxml import html
from collections import defaultdict
import requests
import json
import re
import unicodedata


def decode_diacritics(input_message):
    decoded_message = unicodedata.normalize('NFD', input_message[0]).encode('ascii', 'ignore')
    return decoded_message


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
            transactions[tr[0]]['date'] = tr[1].xpath('td[1]/text()')
            transactions[tr[0]]['amount'] = re.findall('[0-9]+[,][0-9]+', tr[1].xpath('td[2]/text()')[0])
            transactions[tr[0]]['type'] = decode_diacritics(tr[1].xpath('td[3]/text()'))

            transactions[tr[0]]['name'] = tr[1].xpath('td[4]/text()')

        return transactions


print(from_html_to_csv('https://www.fio.cz/ib2/transparent?a=2600088789'))
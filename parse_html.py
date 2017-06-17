from lxml import html
from collections import defaultdict
import requests
import json

def from_html_to_json(url):

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
            for piece in enumerate(structure):
                if piece[0] == 1:
                    transactions[tr[0]][piece[1]] = float(tr[1].xpath('td[2]/@data-value')[0])
                else:
                    try:
                        transactions[tr[0]][piece[1]] = tr[1].xpath('td[{}]/text()'.format(piece[0]+1))[0]
                    except IndexError:
                        pass

        return json.dumps(transactions)

#from_html_to_json('https://www.fio.cz/ib2/transparent?a=2600088789')

print(from_html_to_json('https://www.fio.cz/ib2/transparent?a=2600088789'))

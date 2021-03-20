import xml.etree.ElementTree as ET
from pprint import pprint


PARENT, NO_PARENT, CHILD = range(3)
ONE_OPTION, SELECTORS = range(2)
ID      = "id"
PAR_ID  = "parent"
NAME    = "name"
URL     = "url"
PRICE   = "price"
CURR    = "currencyId"
IMAGE   = "image"
PARAM   = "param"
E_TYPE  = "e_type"
OPTIONS = "options"


def parse_element(elem):
    if "parent" in elem.keys():
        e_type = CHILD
    elif elem.find(PRICE) is not None:
        e_type = NO_PARENT
    else:
        e_type = PARENT

    def parse_child(elem):
        id = elem.get(ID)
        parent = elem.get(PAR_ID)
        name = elem.find(NAME).text
        url = elem.find(URL).text
        image = elem.find(IMAGE).text
        price = elem.find(PRICE).text
        currency = elem.find(CURR).text
        params = {
            t.get(NAME): t.text
            for t in elem.findall(PARAM)
        }
        return {
            E_TYPE: e_type,
            ID: id,
            PAR_ID: parent,
            NAME: name,
            URL: url,
            PRICE: price,
            CURR: currency,
            IMAGE: image,
            PARAM: params
        }

    def parse_parent(elem):
        id = elem.get(ID)
        name = elem.find(NAME).text
        url = elem.find(URL).text
        image = elem.find(IMAGE).text
        return {
            E_TYPE: e_type,
            ID: id,
            NAME: name,
            URL: url,
            IMAGE: image
        }

    def parse_no_parent(elem):
        id = elem.get(ID)
        name = elem.find(NAME).text
        url = elem.find(URL).text
        image = elem.find(IMAGE).text
        price = elem.find(PRICE).text
        currency = elem.find(CURR).text
        return {
            E_TYPE: e_type,
            ID: id,
            NAME: name,
            URL: url,
            PRICE: price,
            CURR: currency,
            IMAGE: image
        }

    return {
        CHILD: parse_child,
        PARENT: parse_parent,
        NO_PARENT: parse_no_parent
    }.get(e_type)(elem)


root = ET.parse('hackathon.xml').getroot()
items = {}
for offer in root.findall('shop/offers/offer'):
    item = parse_element(offer)
    print(item)
    e_type = item[E_TYPE]
    if e_type == PARENT:
        id = item[ID]
        if id not in items:
            items[id] = {E_TYPE: SELECTORS, OPTIONS: []}
        for key, value in item.items():
            items[id][key] = value
    elif e_type == CHILD:
        id = item[PAR_ID]
        if id not in items:
            items[id] = {E_TYPE: SELECTORS, OPTIONS: []}
        obj = {
            ID: item[ID],
            IMAGE: item[IMAGE],
            NAME: item[NAME],
            PRICE: item[PRICE],
            CURR: item[CURR],
            **item[PARAM]
        }
        items[id][OPTIONS].append(obj)
    else:
        id = item[ID]
        obj = {
            E_TYPE: item[E_TYPE],
            ID: item[ID],
            IMAGE: item[IMAGE],
            NAME: item[NAME],
            PRICE: item[PRICE],
            CURR: item[CURR]
        }
        items[id] = obj

with open('output.json', 'wt') as file:
    import json
    json.dump(items, file)
pprint(items)

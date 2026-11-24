import xml.etree.ElementTree as ET
import json, re, sys

NS = {'a': 'http://www.w3.org/2005/Atom'}
INVIS = re.compile('[\u200b\u200c\u200d\u200e\u200f\ufeff\u00ad\u2060\u180e\u202a\u202b\u202c\u202d\u202e\u2066\u2067\u2068\u2069]')

tree = ET.parse(sys.argv[1])
root = tree.getroot()
items = []
for e in root.findall('a:entry', NS):
    t = e.find('a:title', NS)
    title = t.text if t is not None and t.text else ''
    link = ''
    for l in e.findall('a:link', NS):
        if l.get('rel') == 'alternate':
            link = l.get('href')
            break
    if not link:
        ls = e.findall('a:link', NS)
        if ls:
            link = ls[0].get('href', '')
    title = INVIS.sub('', title).strip()
    items.append({'source': 'Reddit', 'title': title, 'url': link, 'score': 0, 'comments': 0})
    if len(items) >= 25:
        break

print(json.dumps(items, ensure_ascii=False, indent=2))
with open(sys.argv[2], 'w', encoding='utf-8') as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

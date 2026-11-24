import json, sys
p = sys.argv[1]
d = json.load(open(p))
print('failures:', d.get('failures'))
print('counts:', {k: len(v) for k, v in d.items() if k != 'failures'})
print()
for k in ['hn', 'devto', 'lobsters', 'github', 'reddit']:
    print('===', k, len(d.get(k, [])))
    for i in d.get(k, [])[:12]:
        print(i.get('score'), '|', i.get('title', '')[:110], '|', i.get('url', '')[:110])

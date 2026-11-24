import re, sys
p = sys.argv[1]
lines = open(p, encoding='utf-8').read().split('\n')
sec = None
counts = {}
bad = []
for ln in lines:
    m = re.match(r'^## ', ln)
    if m:
        sec = ln.strip()
        counts[sec] = 0
        continue
    if re.match(r'^\d+\. ', ln):
        if sec:
            counts[sec] += 1
        if '=<http' not in ln:
            bad.append('URL not wrapped/summary missing: ' + ln[:70])
        if not re.search(r'=<https?://[^>]+>$', ln.strip()):
            bad.append('URL not at line end: ' + ln[:70])
print('sections/counts:')
for k, v in counts.items():
    print('  ', k, v)
print('bad:', len(bad))
for b in bad:
    print('  ', b)
# invisible chars
inv = re.findall(r'[\u200b\u200c\u200d\u200e\u200f\ufeff\u00ad\u2060\u180e]', open(p, encoding='utf-8').read())
print('invisible chars:', len(inv))

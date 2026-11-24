import re, sys, urllib.request

url = sys.argv[1]
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/128.0 Safari/537.36"})
html = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")
# drop script/style/head
html = re.sub(r'(?is)<(script|style|head|nav|footer)[^>]*>.*?</\1>', ' ', html)
html = re.sub(r'(?s)<!--.*?-->', ' ', html)
text = re.sub(r'(?s)<[^>]+>', ' ', html)
text = re.sub(r'&nbsp;', ' ', text)
text = re.sub(r'&amp;', '&', text)
text = re.sub(r'&lt;', '<', text)
text = re.sub(r'&gt;', '>', text)
text = re.sub(r'&#\d+;', ' ', text)
text = re.sub(r'[ \t]+', ' ', text)
text = re.sub(r'\n\s*\n+', '\n', text)
print(text.strip()[:3000])

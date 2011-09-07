import urllib, json
"""Returns latest mtGox USD rate"""
# Get a file-like object for the Python Web site's home page.
f = urllib.urlopen('http://mtgox.com/api/0/data/ticker.php')
# Read from the object, storing the page's contents in 's'.
line=f.read();
u=line.decode('utf-8');
s = json.loads(u)
last=(s['ticker']['last'])
print last



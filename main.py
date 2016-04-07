#!/usr/bin/env python

from lxml import html
import pprint
import urllib
import json

def get_cached(url):
    fname = 'cached/' + url.replace('/', '__')
    try:
        f = open(fname)
        ret = f.read()
    except IOError:
        ret = urllib.urlopen(url).read()
        f = open(fname, "w")
        f.write(ret)
    f.close()
    return ret

def get_laptop(url):
    t = html.fromstring(get_cached(url))
    d = {}
    for r in t.xpath('//td [@class="title"]/..'):
        items = [i.strip() for i in r[1].text_content().strip().split('\n')]
        while '' in items:
            items.remove('')
        d[r[0].text_content()] = items
    return d

def get_devices(starturl, pages = 1):
    for i in range(1, pages + 1):
        if pages != 1:
            url = starturl % i
        else:
            url = starturl
        t = html.fromstring(get_cached(url))
        laptops = t.xpath('//li [contains(@class, "model")]//p')
        for laptop in laptops:
            vendor = laptop.text.strip()
            model = laptop[0].text.strip()
            devicetype = laptop[0].tail.strip()
            url = 'http://www.ubuntu.com' + laptop[0].get('href')
            laptop = get_laptop(url)
            laptop.update({
                'vendor': vendor,
                'model': model,
                'devicetype': devicetype
            })
            print(json.dumps(laptop))

get_devices('http://www.ubuntu.com/certification/desktop/models/?&page=%d', 42)
get_devices('http://www.ubuntu.com/certification/server/models/?&page=%d', 14)
get_devices('http://www.ubuntu.com/certification/smart-device/models/?&page=%d', 14)
get_devices('http://www.ubuntu.com/certification/smart-device/models/?query=&category=Snappy+Ubuntu+Core&category=Ubuntu+Phone&level=Any')

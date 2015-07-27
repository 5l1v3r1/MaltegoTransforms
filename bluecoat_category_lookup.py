#!/usr/bin/env python
#
# Search BlueCoat SiteReview for URL/Domain and return the category
#
#

from MaltegoTransform import *
import sys
import re
import requests
import simplejson

input_url = sys.argv[1]
m = MaltegoTransform()

url = 'https://sitereview.bluecoat.com/rest/categorization'
headers = {'X-Requested-With':'XMLHttpRequest', 
           'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36', 
           'Origin':'https://sitereview.bluecoat.com',
           'Referer':'https://sitereview.bluecoat.com/sitereview.jsp'}

payload = 'url=%s' % (input_url)
r = requests.post(url,headers=headers,data=payload)
response_dict = simplejson.loads(r.text)

try:
    categorization = response_dict.get("categorization", {})
    unrated = response_dict.get("unrated", {})
except:
    m.returnOutput()

if (unrated == 'true'):
    category = 'Unrated'
    m.addEntity('maltego.Phrase', category)
    m.returnOutput()    
else:
    try:
        match = re.match("^.+\>(.+)\<.+", categorization)
        category = match.group(1)
        m.addEntity('maltego.Phrase', category)
        m.returnOutput()        
    except:
        m.returnOutput()


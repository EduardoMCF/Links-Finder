from itertools import count
from sys import stdout
from os import system
import argparse

from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests,lxml
from urllib.parse import urlparse
from datetime import datetime

argParser = argparse.ArgumentParser(description = "A webcrawler to get all links of a page or a group of pages")
argParser.add_argument('--url', action = 'store', dest = 'url',required = True, help = 'The url that you want to be crawled.')
argParser.add_argument('--recursive', action = 'store', dest = 'recursive', default = False, required = False, help = 'If True search in all descendants of the given page, otherwise only return the links of the given page.')
arguments = argParser.parse_args()

def getAllLinks(page : str, recursive=False) -> None:
    if recursive: update()
    try:
        response = requests.get(page,headers=header,timeout=2)
        if response:
            soup = BeautifulSoup(response.content,'lxml')
            if soup.body:
                for aTag in set(soup.body.find_all('a',href=True)).difference(links):
                    link = aTag.get('href')
                    newPage = (domainName + link).strip('/') if link.startswith(anchor) else link
                    if not newPage.startswith(url):
                        link = domainName+link if link.startswith('/') else link
                        otherLinks.add(link)
                    elif newPage.startswith(url) and link not in links:
                        links.add(link)
                        if recursive: getAllLinks(newPage,recursive)
    except Exception:
        fails.add(page)

def update() -> None:
    animation = ['|','/','-','\\']
    stdout.write('\rLoading %s %i Page(s) Processed' %(animation[next(counter)%4],len(links)+len(otherLinks)+len(fails)))
    stdout.flush()

def parseLinks() -> str:
    anchorLinks = 'Same anchor links:\n' + '\n'.join(set(map(lambda x: domainName + x, links.difference({url}))))
    outsideLinks = '\n\nDifferent anchor links:\n' + '\n'.join(otherLinks)
    failLinks = '\n\nError links:\n' + '\n'.join(fails)
    return 'The anchor url was: \n%s\n\n%s' %(url,anchorLinks + outsideLinks + failLinks)

url = arguments.url
if not url.startswith('http'): url  = 'http://' + url
parsedUrl = urlparse(url)
domainName = parsedUrl.scheme+ '://' + parsedUrl.netloc
anchor = '/' + url[len(domainName):].strip('/') if url != domainName else '/'

links,fails,otherLinks = {url},set(),set()
ua = UserAgent()
header = {'user-agent':ua.chrome}

try:
    response = requests.get(url,headers=header,timeout=2)
except Exception:
    raise RuntimeError("Timeout error")

if not response: raise RuntimeError('Error %i' %response.status_code)

counter = count(0,1)
getAllLinks(url,arguments.recursive)

timestamp = datetime.now().strftime('%Y-%b-%d_%H-%M-%S')
fileName = ''.join(filter(lambda x: x not in '<>:"\\/|?*',BeautifulSoup(response.content,'lxml').title.text + '_' + timestamp + '.txt')).strip('. ')
output = open(fileName,'w')
output.write(parseLinks())
output.close()

stdout.write('\rDone! ')
system('pause')



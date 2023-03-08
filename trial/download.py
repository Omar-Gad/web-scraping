# import os, sys, re
# import requests
# from urllib.parse import urljoin
# from bs4 import BeautifulSoup

# def savePage(url, pagepath='page'):
#     def savenRename(soup, pagefolder, session, url, tag, inner):
#         if not os.path.exists(pagefolder): # create only once
#             os.mkdir(pagefolder)
#         for res in soup.findAll(tag):   # images, css, etc..
#             if res.has_attr(inner): # check inner tag (file object) MUST exists  
#                 try:
#                     filename, ext = os.path.splitext(os.path.basename(res[inner])) # get name and extension
#                     filename = re.sub('\W+', '', filename) + ext # clean special chars from name
#                     fileurl = urljoin(url, res.get(inner))
#                     filepath = os.path.join(pagefolder, filename)
#                     # rename html ref so can move html and folder of files anywhere
#                     res[inner] = os.path.join(os.path.basename(pagefolder), filename)
#                     if not os.path.isfile(filepath): # was not downloaded
#                         with open(filepath, 'wb') as file:
#                             filebin = session.get(fileurl)
#                             file.write(filebin.content)
#                 except Exception as exc:
#                     print(exc, file=sys.stderr)
#     session = requests.Session()
#     #... whatever other requests config you need here
#     response = session.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
#     soup = BeautifulSoup(response.text, "html.parser")
#     path, _ = os.path.splitext(pagepath)
#     pagefolder = path+'_files' # page contents folder
#     tags_inner = {'img': 'src', 'link': 'href', 'script': 'src'} # tag&inner tags to grab
#     for tag, inner in tags_inner.items(): # saves resource files and rename refs
#         savenRename(soup, pagefolder, session, url, tag, inner)
#     with open(path+'.html', 'wb') as file: # saves modified html doc
#         file.write(soup.prettify('utf-8'))
        
# savePage('https://www.classcentral.com/', 'classcentral')



# =================================================================================



# import urllib.request as urllib2
# from bs4 import *
# from urllib.parse  import urljoin


# def crawl(pages, depth=None):
#     indexed_url = [] # a list for the main and sub-HTML websites in the main website
#     for i in range(depth):
#         for page in pages:
#             if page not in indexed_url:
#                 indexed_url.append(page)
#                 try:
#                     c = urllib2.urlopen(page)
#                 except:
#                     print( "Could not open %s" % page)
#                     continue
#                 soup = BeautifulSoup(c.read())
#                 links = soup('a') #finding all the sub_links
#                 for link in links:
#                     if 'href' in dict(link.attrs):
#                         url = urljoin(page, link['href'])
#                         if url.find("'") != -1:
#                                 continue
#                         url = url.split('#')[0] 
#                         if url[0:4] == 'http':
#                                 indexed_url.append(url)
#         pages = indexed_url
#     return indexed_url


# pagelist=["https://en.wikipedia.org/wiki/Python_%28programming_language%29"]
# urls = crawl(pagelist, depth=1)
# print( urls )




# =================================================================================

from bs4 import BeautifulSoup
from pip._vendor import requests
import os
import shutil
import re
from bs4 import BeautifulSoup
import uuid

rnd_str = uuid.uuid4().hex
main_name="download_"+rnd_str
main_folder= main_name+"/"
dir = main_folder

if os.path.exists(dir):
    shutil.rmtree(dir)
os.mkdir(main_folder)

headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
site = 'https://www.classcentral.com/'

response = requests.get(site, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
#find all jpg,png,gif
img_tags = soup.find_all('img')
urls = [img['src'] for img in img_tags]
#print (urls)
for url in urls:
    filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)
   #with open( '/home/danesh20016/public_html/ts/'+main_folder+filename.group(1), 'wb') as f:
    print (url)
    with open( './public_html/ts/'+main_folder+filename.group(1), 'wb') as f:
    #with open(main_folder+filename.group(1), 'wb') as f:
        if 'http' not in url:
            # sometimes an image source can be relative
            # if it is provide the base url which also happens
            # to be the site variable atm.
            url = '{}{}'.format(site, url)
        response = requests.get(url)
        f.write(response.content)

 #find all css  
for link in soup.findAll('link', href=True):
#print ("Found the URL:", link['href'])
    if re.search(".css", link['href']):
        print (link['href'])
        with open('/home/danesh20016/public_html/ts/'+main_folder+ filename.group(1), 'wb') as f:
            # with open(main_folder+filename.group(1), 'wb') as f:
            if 'http' not in url:
                # sometimes an image source can be relative
                # if it is provide the base url which also happens
                # to be the site variable atm.
                url = '{}{}'.format(site, link['href'])
            response = requests.get(url)
            f.write(response.content)
#find all js
link_js = [sc["src"] for sc in soup.find_all("script",src=True)]
for link in link_js:
    print ("Found the URL:", link)
    with open('/home/danesh20016/public_html/ts/'+main_folder+ filename.group(1), 'wb') as f:
        # with open(main_folder+filename.group(1), 'wb') as f:
        if 'http' not in url:
            # sometimes an image source can be relative
            # if it is provide the base url which also happens
            # to be the site variable atm.
            url = '{}{}'.format(site, link)
        response = requests.get(url)
        f.write(response.content)

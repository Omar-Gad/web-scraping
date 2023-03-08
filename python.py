import requests
from bs4 import BeautifulSoup
from translatepy import Translator
import re
import logging as logger

logger.basicConfig(level=logger.INFO)

translator = Translator()

def scrape_and_translate(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    }

    logger.info(f"Scraping {url} ...")

    response = requests.get(url, headers=headers)
    html_content = response.text

    logger.info(f"Response returned with {response.status_code}")

    soup = BeautifulSoup(html_content, 'html.parser')

    # for descendent in soup.descendants:
    #     if isinstance(descendent, str) or not descendent:
    #         continue
    #     if descendent.name in ['script', 'style'] or descendent.string in ['\n', '\t']:
    #         continue
    #     if not descendent.string or not descendent.string.strip():
    #         continue
        
    #     print(f'{descendent.string} -> ', end='')
        
    #     descendent.string = translator.translate(descendent.string, "Hindi").result
    #     print(descendent.string)

    
    logger.info("Writing translated HTML to translated.html ...")

    with open('translated.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
    logger.info("Done")

    # # Find all the links in the page and scrape/translate the linked pages recursively
    # for link in soup.find_all('a'):
    #     href = link.get('href')
    #     if href.startswith('http'):
    #         scrape_and_translate(href)


# Define the URL of the website to scrape
url = "https://www.classcentral.com/"

# Scrape and translate the initial page and all linked pages recursively
scrape_and_translate(url)

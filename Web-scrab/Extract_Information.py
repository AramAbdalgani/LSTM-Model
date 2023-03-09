from typing import List, Dict, Union
from bs4 import BeautifulSoup
import requests

def extract_links_and_text(cleaned_html: str) -> List[Dict[str, Union[str, List[str]]]]:
    # parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # find all <a> tags with href attributes
    a_tags = soup.find_all('a', href=True)

    links_and_text = []
    for a in a_tags:
        # find all <img> tags with alt attributes within the current <a> tag
        img_tags = a.find_all('img', alt=True)
        images = [img['alt'] for img in img_tags]

        # find all <img> tags with src attributes within the current <a> tag
        img_tags = a.find_all('img', src=True)
        sources = [img['src'] for img in img_tags]

        # extract the text between the <a> tags
        text = a.text.strip()

        # find the next tag after the current <a> tag
        next_tag = a.find_next()

        # get the text between the current <a> tag and the next tag
        while next_tag.name == 'br':
            next_tag = next_tag.find_next()
        next_text = a.find_next().get_text(strip=True)
        
        # append a dictionary of the current link, its images, its sources, and its text to the list
        links_and_text.append({'link': a['href'], 'images': images, 'sources': sources, 'text': text, 'next_text': next_text})

    # return the list of links and their corresponding images, sources, and text
    return links_and_text

# get the HTML from a URL
url = 'https://www.vox.com/'
html = requests.get(url).text

# extract the links and their corresponding images, sources, and text from the HTML

cleaned_html = clean_html(html)
links_and_text = extract_links_and_text(clean_html)
# print the results
for link_info in links_and_text:
    print( link_info['link'])
    print( link_info['images'])
    print( link_info['sources'])
    print( link_info['text'])
    print( link_info['next_text'])
    print("\n")
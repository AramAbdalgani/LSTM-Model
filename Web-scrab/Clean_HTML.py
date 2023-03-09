import requests
from bs4 import BeautifulSoup

# define the list of allowed tags and attributes
allowed_tags = ['a', 'body', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'head', 'hr', 'html', 'i', 'img', 'li', 'ol', 'p', 'ruby', 'strong', 'table', 'tbody', 'td', 'th', 'title', 'tr', 'ul']
allowed_attrs = ['href', 'src', 'alt', 'width', 'height', 'colspan', 'rowspan']

# define a function to clean the HTML
def clean_html(html):
    # parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # find the header and footer elements and remove them
    header = soup.find('header')
    if header:
        header.decompose()  # remove the header tag and its contents
    footer = soup.find('footer')
    if footer:
        footer.decompose()  # remove the footer tag and its contents

    # fix non-well formed tags and attributes
    for tag in soup.find_all():
        # remove any attributes that are not in the allowed list
        for attr in list(tag.attrs):
            if attr not in allowed_attrs:
                del tag[attr]
        # add an alt attribute to any img tag that doesn't have one
        if tag.name == 'img' and 'alt' not in tag.attrs:
            tag['alt'] = ''

    # convert the markup to HTML5
    if soup.html:
        soup.html['lang'] = 'en'
    if soup.head:
        meta_tag = soup.head.find('meta', attrs={'http-equiv': 'content-type'})
        if meta_tag:
            meta_tag['charset'] = 'UTF-8'

    # reduce the markup to allowed tags
    for tag in soup.find_all():
        if tag.name not in allowed_tags:
            tag.unwrap()  # remove the tag and leave its contents
        elif tag.name == 'b':
            tag.name = 'strong'  # replace b tag with strong tag
        elif tag.name == 'div':
            tag.name = 'p'  # replace div tag with p tag

    # reformat the HTML with proper line breaks and indentation
    return soup.prettify()

#Test the code in here 
#url = 'https://alghad.com/'
#html = requests.get(url).text

# clean the HTML
#cleaned_html = clean_html(html)
#print(cleaned_html)
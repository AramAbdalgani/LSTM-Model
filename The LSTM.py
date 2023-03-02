import requests
from bs4 import BeautifulSoup

# Set the URL of the news website you want to scrape
url = "https://thealike.com/"

response = requests.get(url)

# Create a BeautifulSoup object from the HTML content of the website
soup = BeautifulSoup(response.content, "html.parser")

# Initialize empty list to store the titles and their body structures
titles = []

# Find all HTML tags containing titles on the website
title_tags = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'], class_=lambda x: x not in ['hidden'], id=lambda x: x not in ['hidden'])

# Extract the text content, body structure, and image URL of each title tag and append it to the titles list
for title_tag in title_tags:
    title_text = title_tag.get_text().strip()
    # Exclude titles that are just a few words or contain certain keywords
    if len(title_text.split()) > 3 and "Subscribe" not in title_text and "Log In" not in title_text:
        title_structure = []
        parent_tag = title_tag.parent
        while parent_tag.name != 'html' and parent_tag.name != 'main':
            title_structure.append(parent_tag.name)
            parent_tag = parent_tag.parent
        # Find the previous tag that contains an image
        image_tag = title_tag.find_previous('img')
        if image_tag is not None:
            image_url = image_tag.get('src')
        else:
            image_url = None
        titles.append({'title': title_text, 'structure': title_structure[::-1], 'image_url': image_url})

# Print the extracted titles with their body structures and image URLs
for title in titles:
    print(title['title'])
    print(' --> '.join(title['structure']))
    print('Image URL:', title['image_url'])
    print('\n')
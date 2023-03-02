import requests
from bs4 import BeautifulSoup
import csv
import spacy

# load the spaCy model for tokenization
nlp = spacy.load("en_core_web_sm")

# open the input CSV file
with open('url_news.csv', 'r') as input_file:
    csv_reader = csv.reader(input_file)

    # open the output CSV file
    with open('output.csv', 'w', newline='', encoding='utf-8') as output_file:
        csv_writer = csv.writer(output_file)

        # write the header row
        csv_writer.writerow(['Token', 'Image URL'])

        # loop over each URL in the input CSV file
        for row in csv_reader:
            url = row[0]

            try:
                # make a request to the URL with a timeout of 60 seconds
                response = requests.get(url, timeout=60, verify=False)
                html_content = response.text

                # Remove headers and footers from the HTML content
                soup = BeautifulSoup(html_content, 'html.parser')
                for header in soup.find_all(['header', 'footer']):
                    header.decompose()
                img_urls = [img['src'] if 'src' in img.attrs else None for img in soup.find_all('img')]

                # Tokenize the HTML content
                pairs = []
                for tag in soup.find_all():
                    tokens = []
                    tokens.append('<' + tag.name + '>')
                    for attr, val in tag.attrs.items():
                        tokens.append(f'{attr}="{val}"')
                    if tag.string:
                        tokens.extend(tag.string.split())
                    tokens.append('</' + tag.name + '>')

                    # Append each token with the current image URL to the pairs list if it's an image tag
                    if tag.name == 'img' and 'src' in tag.attrs:
                        for token in tokens:
                            pairs.append((token, tag['src']))

                # Write the token-image pairs to the output CSV file
                csv_writer.writerows(pairs)
                print(pairs)

            except requests.exceptions.ReadTimeout:
                print(f"Timeout occurred for URL: {url}. Skipping...")
                continue




   
   
        
        
import pandas as pd
import nltk 
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import json

# download required nltk data
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('omw')

# load the JSON dataset
data = []
with open('/content/News_Category_Dataset_v3.json') as f:
    for line in f:
        try:
            d = json.loads(line)
            data.append(d)
        except:
            continue
            
data = data[:1000] 

# define a function to extract the desired field from the data
def get_field(data, field):
    return [d[field] for d in data]

# extract the desired fields from the data
links = get_field(data, 'link')
headlines = get_field(data, 'headline')
categories = get_field(data, 'category')
short_descriptions = get_field(data, 'short_description')
authors = get_field(data, 'authors')
dates = get_field(data, 'date')

# vectorize the text data using TfidfVectorizer for each field
vectorizers = {}
models = {}
for field, text in zip(['link', 'headline', 'category', 'short_description', 'authors', 'date'], [links, headlines, categories, short_descriptions, authors, dates]):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(text)
    model = KMeans(n_clusters=6, random_state=0)
    model.fit(X)
    vectorizers[field] = vectorizer
    models[field] = model

# function to predict the field for a given text
def predict_field(text):
    text_vectorized = {}
    for field in ['link', 'headline', 'category', 'short_description', 'authors', 'date']:
        if field in vectorizers:
            text_vectorized[field] = vectorizers[field].transform([text])

    max_score = -1
    predicted_field = None
    for field, vec in text_vectorized.items():
        if vec is not None:
            score = models[field].score(vec)
            if score > max_score:
                max_score = score
                predicted_field = field

    if predicted_field is None:
        field_name = 'Invalid field'
    else:
        field_name = predicted_field

    return "Predicted field for text '%s': %s" % (text, field_name)

#if you want to test on a random infromation
#print(predict_field("Apple releases new iPhone"))


#print(predict_field("http://www.example.com"))

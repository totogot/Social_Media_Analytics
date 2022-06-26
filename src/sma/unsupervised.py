import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import emoji
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.tokenize import word_tokenize
from sklearn.cluster import KMeans
import unidecode
import spacy
import contractions
import string

nlp = spacy.load('en_core_web_sm')



def clean_tweet(tweet):
    # replace new line characters with space
    cleaned_tweet = tweet.strip().replace('\n', ' ')
    # convert to lower
    cleaned_tweet = cleaned_tweet.lower()
    # remove all tags
    cleaned_tweet = re.sub(r"@([A-Za-z0-9_]{1,50})", '', cleaned_tweet)
    # clean out all cashtags
    cleaned_tweet = re.sub("\$[A-Za-z]{1,5}", '', cleaned_tweet)
    # remove all links
    cleaned_tweet = re.sub(r'http\S+', '', cleaned_tweet)
    # remove emojis
    cleaned_tweet = emoji.replace_emoji(cleaned_tweet, replace = '')
    # convert accented characters to ASCII characters
    cleaned_tweet = unidecode.unidecode(cleaned_tweet)
    #expand contractions
    cleaned_tweet = contractions.fix(cleaned_tweet)
    # remove stop words and words length = 1
    all_stopwords = nlp.Defaults.stop_words
    cleaned_tweet = ' '.join([word for word in cleaned_tweet.split() if word not in (all_stopwords)])
    # lemmantize the tweet
    doc = nlp(cleaned_tweet)
    cleaned_tweet = ' '.join([word.lemma_ for word in doc])
    # keep only letters
    cleaned_tweet = re.sub(r'[^a-zA-Z ]+', '', cleaned_tweet)
    # remove any remaining punctuation
    cleaned_tweet = cleaned_tweet.translate(str.maketrans('', '', string.punctuation))
    # remove excessive white space
    cleaned_tweet = re.sub(' +', ' ', cleaned_tweet)
    # convert to lower again to in the case that removing special characters has introduced CAPs
    cleaned_tweet = cleaned_tweet.lower()

    return cleaned_tweet


def obtain_tweet_vector(tokens, model):
    
    vectors = []
    for token in tokens:
        if token in model.wv:
            vectors.append(model.wv[token])
        else:
            continue

    average_vector = np.asarray(vectors).mean(axis=0)

    return average_vector


def plot_elbow(vectors, max_clusters, model_type='lloyd'):

    K = range(1,max_clusters)
    distortions = []
    i = 1
    for k in K:
        print(f'Computing distortions {str(i)} / {max_clusters}')
        kmeans = KMeans(n_clusters=k, algorithm = model_type, random_state=0)
        kmeans.fit(vectors)
        distortions.append(kmeans.inertia_)
        i= i+1

    plt.figure(figsize=(16,8))
    plt.plot(K, distortions, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Distortion')
    plt.title('The Elbow Method showing the optimal k')
    plt.show()

    return
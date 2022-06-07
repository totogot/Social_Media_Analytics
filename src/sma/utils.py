from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import re
import emoji
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import contractions



def scrape_stock_tickers():

    #state the site url
    url="https://stockanalysis.com/stocks/"

    #fetch html for webpage
    html_content = requests.get(url).text

    #parse html
    soup = BeautifulSoup(html_content, "lxml")
    script = soup.find("script", {"id": "__NEXT_DATA__"})
    data = json.loads(script.text)

    stock_table = pd.DataFrame(data['props']['pageProps']['stocks'])
    stock_table = stock_table.rename(columns={'s': 'ticker', 'n': 'name', 'm': 'market_cap', 'i': 'industry'})

    return stock_table


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
    # remove hastags
    cleaned_tweet = re.sub('#[A-Za-z0-9_]+', '', cleaned_tweet)
    # remove emojis
    cleaned_tweet = re.sub(emoji.get_emoji_regexp(), '', cleaned_tweet)
    # expand contractions
    cleaned_tweet = contractions.fix(cleaned_tweet)
    # remove punctuation
    cleaned_tweet = cleaned_tweet.translate(str.maketrans('', '', string.punctuation))
    # keep only letters
    cleaned_tweet = re.sub(r'[^a-zA-Z ]+', '', cleaned_tweet)
    # remove excessive white space
    cleaned_tweet = re.sub(' +', ' ', cleaned_tweet)

    return cleaned_tweet


def tokenize_tweet(clean_tweet):

    # perform tokenization
    tokenized_tweet = word_tokenize(clean_tweet)
    # remove stop words
    stop_words = stopwords.words('english')
    tokenized_tweet = [word for word in tokenized_tweet if word not in (stop_words)]
    # perform stemming
    stemmed_tweet = ' '.join([PorterStemmer().stem(word) for word in tokenized_tweet])

    return stemmed_tweet

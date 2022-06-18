import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
import re


def vader_preprocess(text):
    """
    basic cleaning to remove tags, and links that may be incorrectly analysed for sentiment.
    as a lexicon based approach, VADER does not require tokensiation or lemmatisation, and
    can handle the likes of emojis

    :param text: str object containing the text we wish to clean
    """

    # replace new line characters with space
    clean_text = text.strip().replace('\n', ' ')
    # convert to lower
    clean_text = clean_text.lower()
    # remove all tags
    clean_text = re.sub(r"@([A-Za-z0-9_]{1,50})", '', clean_text)
    # clean out all cashtags
    clean_text = re.sub("\$[A-Za-z]{1,5}", '', clean_text)
    # remove all links
    clean_text = re.sub(r'http\S+', '', clean_text)
    # remove excessive white space
    clean_text = re.sub(' +', ' ', clean_text)

    return clean_text


def vader_sentiment(text, return_polarities = False):
    """
    runs sentiment classification using VADER for social media analysis
    :param text: str object containin the text we wish to analysis
    :return: dict object containing the polarity outputs from the model
    """

    clean_text = vader_preprocess(text)

    # initiate the vader lexicon model
    sia = SentimentIntensityAnalyzer()

    # obtain polarities
    polarity_dict = sia.polarity_scores(clean_text)

    # define sentiment based on compound polarity
    if polarity_dict['compound'] > 0.1:
        sentiment = 'Positive'
    elif polarity_dict['compound'] < -0.1:
        sentiment = 'Negative'
    else:
        sentiment= 'Neutral'

    # return outputs based on kwarg provided
    if return_polarities == False:
        return sentiment
    elif return_polarities == True:
        return  polarity_dict['pos'], polarity_dict['neg'], polarity_dict['neu'], polarity_dict['compound'], sentiment
    else:
        raise ValueError("'return_polarities' variable must be Boolean value of 'True' or 'False'")
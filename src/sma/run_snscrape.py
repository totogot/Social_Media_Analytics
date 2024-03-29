import numpy as np
from snscrape.modules import twitter as sntwitter
# from snscrape.modules import instagram as sninstagram, facebook as snfacebook, reddit as snreddit
import pandas as pd
import itertools


def validate_twitter_args(terms, username, date_range):
    """
    function for checking the input parameters and reporting any issues with arguments provided

    :param terms: str or list or None object represents the term(s) to be searched for
    :param username: stror None object that represents the username (excluding the "@") who's account to search
    :param date_range: list object containing to str that represent the start and end date in which to search
    """

    #validate that the terms arg is a list of strings
    if terms != None:
        if isinstance(terms, str):
            print("single 'term' provided. pulling posts containing '{}'".format(terms))
        elif isinstance(terms, list):
            if all(isinstance(item, str) for item in terms):
                print("list of 'terms' provided. pulling posts containing each term")
            else:
                raise TypeError("'terms' variable must be a single string or list of strings")
        else:
            raise TypeError("'terms' variable must be a single string or list of strings")
    else:
        print("no 'terms' variable provided. pulling all posts")

    #validate that, if defined, the username is a string
    if username != None:
        if not isinstance(username, str):
            raise TypeError("can only provide 'username' argument of type str")
    else:
        print("no 'username' provided. pulling tweets from all accounts")

    # validate that, if defined, the date_range is a list of 2 string dates
    if date_range != None:
        if not isinstance(date_range, list):
            raise TypeError("'date_range' variable must be a list of 2 dates in str format e.g. ['2022-01-31','2022-02-28']")
        elif len(date_range) != 2:
            raise TypeError("'date_range' variable must be a list of 2 dates in str format e.g. ['2022-01-31','2022-02-28']")
        else:
            if not all(isinstance(item, str) for item in date_range):
                raise TypeError(
                    "'date_range' variable must be a list of 2 dates in str format e.g. ['2022-01-31','2022-02-28']")

    return


def create_twitter_query(terms, username, date_range, lang):
    """
    function for creating the API payload to pull the relevant tweets

    :param terms: str or list or None object represents the term(s) to be searched for
    :param username: stror None object that represents the username (excluding the "@") who's account to search
    :param date_range: list object containing to str that represent the start and end date in which to search
    :param lang: str indicating the two letter abbreviation for the laguage of tweets you want to pull
    :return: str object containing the payload to pass to the SNScrape API
    """

    # create components of the search query
    query_components = []

    # add each section of the query
    if terms != None:
        if isinstance(terms, str):
            query_components.append(terms)
        else:
            query_components.append(' OR '.join(terms))

    if username != None:
        query_components.append('from:{}'.format(str(username).replace('@', '')))

    if date_range != None:
        query_components.append('since:{0} until:{1}'.format(date_range[0], date_range[1]))

    if lang != None:
        query_components.append('lang:{}'.format(lang))

    #combine all provided components into a single query
    query_string = ' '.join(query_components)

    return query_string


def scrape_twitter(terms=None, username=None, date_range=None, lang='en', limit=1000):

    '''
    fucntion to pull tweets given several parameters
    makes use of the following: https://github.com/igorbrigadir/twitter-advanced-search

    :param terms: str or list or None object represents the term(s) to be searched for
    :param username: stror None object that represents the username (excluding the "@") who's account to search
    :param date_range: list object containing to str that represent the start and end date in which to search
    :param lang: str indicating the two letter abbreviation for the laguage of tweets you want to pull
    :param limit: int object to indicate the maximum number of tweets to pull
    :return: dataframe containing the pulled tweet information
    '''

    #ensure the arguments have been provided in the correct format
    validate_twitter_args(terms, username, date_range)

    #create the search query
    query = create_twitter_query(terms, username, date_range, lang)

    #run the search
    scraped_tweets = itertools.islice(sntwitter.TwitterSearchScraper(query).get_items(), limit)
    response_df = pd.DataFrame(scraped_tweets)

    return response_df
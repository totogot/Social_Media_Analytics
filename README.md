# SocialAnalytics

Repository showing a example project developed to analyse Twitter content on a specific company. This project gives a view of how to leverage open-source packages to pull tweets, run unsupervised clustering to develop training data, and utilise the training data to build supervised classifiers for tagging future data.

The main.ipynb contains the run code, with accompanying commentary, while the sma package contains helper functions and wrappers.

## Initial setup
The first thing you are going to want to do is clone this repository, and then set up a virtual environment for installing all package requirements into.

```
$ git clone https://github.com/totogot/Social_Media_Analytics.git
$ cd C:/Users/totogot/Documents/Social_Media_Analytics
$ python -m venv venv
```

Then from within the terminal command line within your IDE (making sure you are in the project folder), you can install all the dependencies for the project, by simply activating the venv and leveraging the setuptools package and the setup.cfg file created in the project repo. 

```
$ .\venv\Scripts\activate
$ pip install --upgrade pip
$ pip install .
```

Note: for IDEs where the CLI uses PowerShell by default (e.g. VS Code), in order to run Activate.ps1 you may find that you first need to update your settings such that Command Prompt is the default terminal shell - see here: https://support.enthought.com/hc/en-us/articles/360058403072-Windows-error-activate-ps1-cannot-be-loaded-because-running-scripts-is-disabled-UnauthorizedAccess-

The last command above will install all dependencies outlined in the setup.cfg file. (ipykernel has been included to enable the main.ipynb to be run also and for relevant visualisations to be outputted also)

## Pulling tweets
To pull posts from social media, I have opted to use the wonderful SNScrape package (https://github.com/JustAnotherArchivist/snscrape) - which comes with a nice Python wrapper to allow users to scrape social media content from across a range of channels (Twitter, Instagram, Facebook, Reddit, Telegram, etc.).

However, from previous experience working in the space, extracting useful insight from the text alone becomes increasingly problematic for channels where additional context is required to get an idea of the messaging - such as visual content (e.g. Instagram), or whole threads (e.g. Reddit). As a result, for simplicity sake, this project will focus only on Twitter posts.

"But since you're only focusing on Twitter, why not use the other libraries out there?" Having experimented somewhat with other Python libraries such as Twint or Tweepy, I found that they can run into a certain compatibility issues, depending on the IDE you executing your code from, and return less detailed attributed from the tweets. My view is that each library has its place and is fit for purpose in different circumstances - but for the purpose of this project we will run with SNScrape


## Guidance
The main.ipynb file contains an annotated notebook with step-by-step comments that outline the approach take, and reasoning behind the choices made
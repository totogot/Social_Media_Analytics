## SocialAnalytics

# Initial setup
The first thing you are going to want to do is set up a virtual environment for installing all package requirements into

```
$ cd C:\Users\jdoe\Documents\PersonalProjects\Social_Analytics
$ python -m venv venv
```

Then from within the terminal command line within your IDE (making sure you are in the project folder), you can install all the dependencies for the project, by simply activating the venv and leveraging the setuptools package and the setup.cfg file created in the project repo. 
Note: for IDEs where the CLI uses PowerShell by default (e.g. VS Code), in order to run Activate.ps1 you may find that you first need to update your settings such that Command Prompt is the default terminal shell - see here: https://support.enthought.com/hc/en-us/articles/360058403072-Windows-error-activate-ps1-cannot-be-loaded-because-running-scripts-is-disabled-UnauthorizedAccess-

```
$ .\venv\Scripts\activate
$ pip install --upgrade pip
$ pip install .
```

This last command will install all dependencies outlined in the setup.cfg file. I have included ipykernel in there to enable the scripts to be run from notebooks also.

# Pulling tweets
To pull posts from social media, I have opted to use the wonderful SNScrape package (https://github.com/JustAnotherArchivist/snscrape) - which comes with a nice Python wrapper to allow users to scrape social media content from across a range of channels (Twitter, Instagram, Facebook, Reddit, Telegram, etc.).

However, from previous experience working in the space, extracting useful insight from the text alone becomes increasingly problematic for channels where additional context is required to get an idea of the messagin - such as visual content (e.g. Instagram), or whole threads (e.g. Reddit). As a result, for simplicity sake, this project will focus only on Twitter posts.

"But since you're only focusing on Twitter, why not use the other libraries out there?" Having experimented somewhat with other Python libraries such as Twint or Tweepy, I found that they can run into a certain compatibility issues, depending on the IDE you executing your code from, and return less detailed attributed from the tweets. My view is that each library has its place and is fit for purpose in different circumstances - but for the purpose of this project we will run with SNScrape



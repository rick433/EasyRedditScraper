# Easy Reddit Scraper

A simple scraper to download media from subreddits.

Installing:

`pip install git+https://github.com/rick433/EasyRedditScraper`.

Example:

```python 
from EasyRedditScraper import Scraper
from EasyRedditScraper.mediatypes import Image, Video

subreddit = "Damnthatsinteresting" #subreddit to be scraped
media_types = [Image(), Video()] #scraping images and videos

my_scraper = Scraper(subreddit=subreddit, media_types=media_types) #initialize the scraper
my_scraper.scrape(pages=2, sort_option="top") #scrape posts from two pages of top posts

``` 

## Customizing to specific subreddits

Currently, downloading of Images (JPG), Videos (MP4) and JSON is supported and predefined classes can be imported via

```python 
from EasyRedditScraper.mediatypes import Image, Video, JSON
``` 

If a post does not match a class the download will be skipped. For some subreddits one might want to create a custom way
of extracting data from a single post, for example, if an external link is providing the data (such as embedded youtube
links). Then one can create a custom class to extract the source of the data:

```python 
from EasyRedditScraper.mediatypes import MediaType

class MyDownloadFormat(MediaType):
    def __init__(self):
        super().__init__(name="NameForFormat") # files will be saved to data/name
        
    def get_url_and_path(self, item): #item is the json data for a single post
        url = ..., #extract url from item. E.g. item['preview']['images'][0]['source']['url']
        filename = ... #how should the file be saved? 
        return [url], [filename] # needs to be a list, could also store multuple items 
        
subreddit = ...
my_scraper = Scraper(subreddit=subreddit, media_types=[MyDownloadFormat()]) #initialize the scraper
my_scraper.scrape(pages=2, sort_option="top") #scrape posts from two pages of top posts if possible
``` 

The data will be saved to `data/subreddit/NameForFormat`.


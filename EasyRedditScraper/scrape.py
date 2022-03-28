import os
import random
import string
import sys
from pathlib import Path
from typing import Tuple, Dict, List

import requests
from tqdm import tqdm

from EasyRedditScraper.mediatypes import MediaType, Content


class Scraper():
    def __init__(self, subreddit: str, media_types: List[MediaType], silent: bool = True):
        """
        :param subreddit: The desired subreddit to be scraped
        :param media_types: List of Media Types (e.g. Image or Video) that should be downloaded
        :param silent: Set to 'False' if details should be printed.
        """
        self.subreddit = subreddit
        self.media_types = media_types
        self.path = os.path.join(os.getcwd(), "data", subreddit)
        # create subfolders for different media types such as image, html, video....
        for type in media_types:
            Path(os.path.join(self.path, type.name)).mkdir(exist_ok=True, parents=True)
        self.stats = {"successful": 0, "failed": 0, "existed": 0}
        self.silent = silent
        self.tqdm_bar = None

    def print_message(self, message: str) -> None:
        """
        Optional printing
        :param message: message that should be printed
        :return:
        """
        if self.silent:
            return None
        else:
            print(message)

    def scrape(self, pages: int = 1, sort_option: str = "new") -> None:
        """
        Download from the subreddit
        :param pages: Number of pages that are scraped. Each page contains 25 posts/items.
        :param sort_option: Sorting, one of ["new","top","hot","controversial"]
        :return: None
        """
        after = None
        self.tqdm_bar = tqdm(total=pages * 25, file=sys.stdout)
        for _ in range(pages):
            json, after = self.get_json(sort_option=sort_option, after=after)
            self.save(json)
        successful = self.stats["successful"]
        failed = self.stats["failed"]
        existed = self.stats["existed"]
        message = f"Successfully download {successful} files. {existed} resources already existed and were skipped. {failed} files could not be downloaded."
        print(message)

    def get_json(self, sort_option: str, after: str) -> Tuple[dict, str]:
        """
        Get json file from reddit api
        :param sort_option: sorting
        :param after: after parameter
        :return: jsonfile, new 'after' string
        """
        agent = "".join(
            [random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in
             range(10)])
        url = 'https://www.reddit.com/r/' + self.subreddit + '/' + sort_option + '.json'
        if after is not None:
            url += f"?after={after}"
        try:
            jsonfile = requests.get(url, headers={'user-agent': agent}).json()
            after = jsonfile['data']['after']
        except Exception as e:
            print(f"Could not connect to {url}. The following exception occured:\n{e}")
            sys.exit()
        return jsonfile, after

    def save(self, json: Dict) -> None:
        """
        extracts links in json and tries to save as the given media types in self.media_types
        :param json: Dict/Json from reddit api that stores item information
        :return: None
        """
        for item in json['data']['children']:
            item = item['data']
            for media_type in self.media_types:
                try:
                    url, filename = media_type.get_url_and_path(item)
                except Exception as error_message:
                    message = "Could not get url due to the following errror: \n" + str(
                        error_message) + "\n Skipping this item and jump to the next one."
                    self.print_message(message)
                    self.stats["failed"] += 1
                    continue
                try:
                    save_path = os.path.join(self.path, media_type.name, filename)
                    success = self.DownloadFile(url, save_path)
                    if success:
                        self.stats["successful"] += 1
                    else:
                        self.stats["existed"] += 1
                except:
                    message = media_type.exception(url)
                    self.stats["failed"] += 1
                    self.print_message(message)

            self.tqdm_bar.update(1)

    def DownloadFile(self, resource, save_path: str) -> bool:
        """
        Download file and save it.
        :param resource: either Content class object or url
        :param save_path: path for saving
        :return: True if download was successful, False if files already existed
        """
        if os.path.exists(save_path):
            message = f"Path {save_path} already exists. Skip download."
            self.print_message(message)
            return False
        if type(resource) == str:
            resource = resource.replace('amp;', '')
            f = requests.get(resource)
            if f.status_code == 200:
                with open(save_path, 'wb') as media_file:
                    for chunk in f.iter_content(100000):
                        media_file.write(chunk)
                self.print_message(f"Downloaded {resource}.")
                return True
        elif type(resource) == Content and len(resource.content) > 0:
            with open(save_path, 'w') as media_file:
                media_file.write(resource.content)
            return True
        return False

import json
from typing import Tuple, Dict


class Content():
    """
    Helper Class to pass on text content and distinguish from url text
    """

    def __init__(self, content=None):
        """
        :param content: Stores human readable data, e.g. html or csv as python string
        """
        self.content = content


class MediaType():
    """
    Base Class to account for varieties of media types and external resources that can be downloaded.
    Makes downloading specific formats more flexible.
    """

    def __init__(self, name: str):
        self.name = name

    def get_url_and_path(self, item: Dict) -> Tuple[str, str]:
        """
        Needs to be overwritten
        :param item: json/dict from the reddit api
        :return: url or content and the path for saving
        """
        return "", ""

    def exception(self, url: str) -> str:
        """
        :param url:
        :return: Exception that can be printed if resource cannot be downloaded as the specified media type
        """
        message = f"Could not download {url} as {self.name}. Skipping. \n"
        return message


class JSON(MediaType):
    """
    Class for saving the json provided by the reddit api
    """

    def __init__(self):
        super().__init__(name="JSON")

    def get_url_and_path(self, item: Dict) -> Tuple[Content, str]:
        subreddit_id = item['subreddit_id']
        id = item['id']
        content = Content(json.dumps(item))
        filename = "_".join([subreddit_id, id]) + ".json"
        return content, filename


class Text(MediaType):
    """
    Class for downloading text
    """

    def __init__(self):
        super().__init__(name="Text")

    def get_url_and_path(self, item: Dict) -> Tuple[Content, str]:
        subreddit_id = item['subreddit_id']
        id = item['id']
        title = item["title"]
        text = item["selftext"]
        content = Content(title + "\n" + text)
        filename = "_".join([subreddit_id, id]) + ".txt"
        return content, filename


class Image(MediaType):
    """
    Class for downloading and saving images. Works with jpg files.
    """

    def __init__(self):
        super().__init__(name="Image")

    def get_url_and_path(self, item: Dict) -> Tuple[str, str]:
        subreddit_id = item['subreddit_id']
        id = item['id']
        url = item['preview']['images'][0]['source']['url']
        filename = "_".join([subreddit_id, id]) + ".jpg"
        return url, filename


class Video(MediaType):
    """
    Class for downloading videos. Works with mp4 files.
    """

    def __init__(self):
        super().__init__(name="Video")

    def get_url_and_path(self, item: Dict) -> Tuple[str, str]:
        subreddit_id = item['subreddit_id']
        id = item['id']
        if item["is_video"]:
            url = item["media"]["reddit_video"]["fallback_url"]
        else:
            url = item['preview']['reddit_video_preview']['fallback_url']
        filename = "_".join([subreddit_id, id]) + ".mp4"
        return url, filename

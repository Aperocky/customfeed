# Define common function and data structures.
import time
import requests
from bs4 import BeautifulSoup

header = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0. 2357.134 Safari/537.36"}

def get_soup(url):
    r = requests.get(url, headers=header)
    soup = BeautifulSoup(r.content, "html.parser")
    return soup

class NewsObject:

    # A news object in a structured way.
    def __init__(self, title, href, contents=None):
        self.title = title
        self.href = href # Use this as identifier.
        self.contents = contents # Holds whatever attributes that comes in.
        self.created_time = time.time() # remember created time.
        self.weight = 0

    @staticmethod
    def packContent(summary=None, content=None, timestamp=None, **kwargs):
        contents = {
            "summary": summary,
            "content": content,
            "timestamp": timestamp
        }
        if kwargs:
            contents.update(kwargs)
        return contents

    def __str__(self):
        contents = ["timestamp", "summary", "content"]
        contentstr = ["\n".join(self.contents[e]) if e == "content" else
                      self.contents[e] for e in contents]
        selfstr = [self.title, self.href] + contentstr
        selfstr = [e for e in selfstr if e is not None]
        return "\n".join(selfstr)

    def calculate_weights(self):
        # TODO: somehow calculate an importance.
        pass

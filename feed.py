# Crawl from source in real time.
from crawling import reuters
import time

class Feeder:

    # This class should be controlled by a controller

    def __init__(self, time_threshold=3600):
        self.queue = {} # Hold current queue of news.
        self.threshold = time_threshold # Keep the news for this many seconds.

    def crawl(self): # Wrap threading around later.
        currentReuter = reuters.run() # returns a list of NewsObject.

        # space for future crawlers. #
        #                            #
        # space for future crawlers. #

        current = {e.href: e for e in currentReuter}
        # Updates queue.
        self.queue.update({k:v for k, v in current.items() if k not in self.queue})

    def purge(self): # Purges older news.
        def purgefunc(news):
            if time.time() - news.created_time > self.threshold:
                return False # Don't keep
            return True
        self.queue = {k:v for k, v in self.queue.items() if purgefunc(v)}

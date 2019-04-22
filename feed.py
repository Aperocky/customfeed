# Crawl from source in real time.
from crawling import reuters
import time
import json
from data import dummy_vector

class Feeder:

    # This class should be controlled by a controller
    def __init__(self, time_threshold=7200):
        self.queue = {} # Hold current queue of news.
        self.threshold = time_threshold # Keep the news for this many seconds.
        self.test_counter = 0 # Dummy var for test

    def crawl(self): # Wrap threading around later.
        existing = set(self.queue.keys())
        currentReuter = reuters.run(existing) # returns a list of NewsObject.

        # space for future crawlers. #
        #                            #
        # space for future crawlers. #

        current = {e.href: e for e in currentReuter}
        self.queue.update({k:v for k, v in current.items() if k not in self.queue})

    # Set news priority if not set.
    def set_priority(self):
        # TODO: tempted to do multiprocessing here, we'll see how slow this is
        for news in self.queue.values():
            if not news.weight_set:
                news.calculate_weights(dummy_vector)

    def purge(self): # Purges older news.
        def purgefunc(news):
            if time.time() - news.created_time > self.threshold:
                return False # Don't keep
            return True
        self.queue = {k:v for k, v in self.queue.items() if purgefunc(v)}

    def test(self):
        # Test the Feeder object.
        self.test_counter += 1
        timestr = str(int(time.time()))
        if not self.test_counter % 2:
            articles = [(e.title, e.href, len(e.contents["content"]))
                        for e in self.queue.values()]
            json.dump(articles, open("testdir/test_{}_{}".format(self.test_counter, timestr), "w"))

    def sortedqueue(self):
        # return a sorted list of queue (not too large, should be easy to sort)
        # this queue will also be json serializable
        # (cutting some lack by not implementing priority queue.)
        listnews = list(self.queue.values())
        listnews.sort(reverse=True)
        return [e.tojson() for e in listnews]

# Define common function and data structures.
import time
import requests
import re
import math
from collections import Counter
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

    def flatten_content(self):
        return "\n".join(self.contents["content"])

    def keyword_extractor(self):
        # Extract the top word from the article.
        # Only works for english btw..mfw ^z^
        currmerge = "\n".join(self.title,
            self.contents["summary"], self.flatten_content())
        wordsplits = re.split("[\s\n\/\(\)\{\}'’]", currmerge.lower())
        dc = Counter(wordsplits)
        delkeys = ["the", "to", "and", "of", "in", "after", "then",
                   "between", "by", "", "a", "an", "will", "it", "that",
                   "which", "on", "were", "was", "had", "have", "new", "-",
                   "s", "as", "its", "for", "but", "at"]
        for k in delkeys: del dc[k]
        keywords = [x[0] for x in dc.most_common(5)]
        self.contents["keywords"] = keywords

    def calculate_weights(self, vector, sectionimportance=None):
        """
        vector: {word: weight} pairs.
        """
        # Use common wordvec techniques.
        weight = self.weight # Do not overwrite this as this could be preset.
        # Sectional effect on scoring.
        if sectionimportance is None:
            sectionimportance = {
                "title": 5,
                "summary": 2,
                "content": 1
            }

        def applywordvec(inputstr, vector):
            # Assuming my vector doesn't grow beyond 100~ keywords. Regex loop should work fine.
            # print(inputstr, vector)
            if inputstr is None:
                return 0
            fitscore = 0
            inputstr = inputstr.lower()
            for k, w in vector.items():
                # INPUT SHOULD BE REGEX STRINGS. cuz why not.
                occurence = len(re.findall(k, inputstr))
                if occurence:
                    fitscore += math.log(occurence+1) * w
            return fitscore

        weight += sectionimportance["title"] * applywordvec(self.title, vector)
        weight += sectionimportance["summary"] * applywordvec(self.contents["summary"], vector)
        weight += sectionimportance["content"] * applywordvec(self.flatten_content(), vector)
        self.weight = weight

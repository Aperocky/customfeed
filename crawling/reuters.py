# GET REUTERS SOURCE.
from bs4 import BeautifulSoup
import requests # apparently reuters doesn't need selenium.
import sys
sys.path.append("..") # To run main test.
from utils import NewsObject

REUTER_MARKET = "https://www.reuters.com/finance/markets"

def get_soup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    return soup

def reuter_extract_headlines(soup):
    # Return a list of NewsObject
    headlines = []
    # The top story of the block.
    try:
        top_story = soup.select(".olympics-topStory h2 a")[0]
        title = top_story.text
        href = REUTER_MARKET + top_story["href"]
        top = NewsObject(title, href)
        headlines.append(top)
    except Exception as e:
        print("Error in getting the top story: {}".format(e))

    # The list of stories that follows the top.
    more_headlines = soup.select(".more-headlines ul li")
    for each in more_headlines:
        try:
            sub = each.select("a")[0]
            title = sub.text
            href = REUTER_MARKET + sub["href"]
            timestamp = each.select(".timestamp")[0].text
            top = NewsObject(title, href, timestamp=timestamp)
            headlines.append(top)
        except Exception as e:
            print("Error in getting more headlines: {}".format(e))
    return headlines

def reuter_extract_blocks(soup, areaid):
    area_news = []
    contents = soup.select("#{} .story-content".format(areaid))
    for each in contents:
        try:
            href = each.select("a")[0]["href"]
            title = each.select("h3")[0].text.strip()
            summary = each.select("p")[0].text
            timestamp = each.select(".timestamp")[0].text
            news = NewsObject(title, href, timestamp=timestamp, summary=summary)
            area_news.append(news)
        except Exception as e:
            print("Error in getting {} data: {}".format(areaid, e))
    return area_news

def run():
    soup = get_soup(REUTER_MARKET)
    master_list = []
    master_list.extend(reuter_extract_headlines(soup))
    blocks = ["tab-markets-us", "tab-markets-emea", "tab-markets-asia"]
    for each in blocks:
        master_list.extend(reuter_extract_blocks(soup, each))
    return master_list

if __name__ == "__main__":
    newslist = run()
    for e in newslist:
        print(e.key)
        print(e.href)
        print(e.timestamp)

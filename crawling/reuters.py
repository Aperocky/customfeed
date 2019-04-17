# GET REUTERS SOURCE.
from bs4 import BeautifulSoup
import requests # apparently reuters doesn't need selenium.
import sys
sys.path.append("..") # To run main test.
from utils import NewsObject

REUTER_MARKET = "https://www.reuters.com/finance/markets"
header = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0. 2357.134 Safari/537.36"}

def get_soup(url):
    r = requests.get(url, headers=header)
    soup = BeautifulSoup(r.content, "html.parser")
    return soup

def get_content(url):
    r = requests.get(url, headers=header)
    soup = BeautifulSoup(r.content, "html.parser")
    article = soup.select(".StandardArticleBody_body > p")
    paragraphs = [p.text for p in article]
    return paragraphs

def reuter_extract_headlines(soup):
    # Return a list of NewsObject
    headlines = []
    # The top story of the block.
    try:
        top_story = soup.select(".topStory h2 a")[0]
        title = top_story.text
        href = REUTER_MARKET + top_story["href"]
        summary = soup.select(".topStory > p")[0].text
        content = get_content(href)
        contents = NewsObject.packContent(content=content, summary=summary)
        top = NewsObject(title, href, contents)
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
            content = get_content(href)
            contents= NewsObject.packContent(content=content, timestamp=timestamp)
            top = NewsObject(title, href, contents)
            headlines.append(top)
        except Exception as e:
            print("Error in getting more headlines: {}".format(e))
    return headlines

def reuter_extract_blocks(soup, areaid):
    area_news = []
    contents = soup.select("#{} .story-content".format(areaid))
    for each in contents:
        try:
            href = REUTER_MARKET + each.select("a")[0]["href"]
            title = each.select("h3")[0].text.strip()
            summary = each.select("p")[0].text
            timestamp = each.select(".timestamp")[0].text
            content = get_content(href)
            contents = NewsObject.packContent(summary=summary, timestamp=timestamp, content=content)
            news = NewsObject(title, href, contents)
            area_news.append(news)
        except Exception as e:
            print("Error in getting {} data: {}".format(areaid, e))
    return area_news

# process the page REUTER_MARKET.
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
        print(e.title)
        print(e.href)
        print(e.contents["summary"])

# GET REUTERS SOURCE.
import sys
sys.path.append("..") # To run main test.
from utils import NewsObject, get_soup
from multiprocessing.pool import ThreadPool

REUTER_MARKET = "https://www.reuters.com/finance/markets"
REUTER_HOME = "https://www.reuters.com"
REUTER_BUSINESS = "https://www.reuters.com/finance"
REUTER_TECH = "https://www.reuters.com/news/technology"
REUTER_BREAKINGVIEW = "https://www.reuters.com/breakingviews"

def reuter_extract_market_headlines(soup):
    # Return a list of NewsObject
    headlines = []
    # The top story of the block.
    try:
        top_story = soup.select(".topStory h2 a")[0]
        title = top_story.text
        href = REUTER_HOME + top_story["href"]
        summary = soup.select(".topStory > p")[0].text
        contents = NewsObject.packContent(summary=summary)
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
            href = REUTER_HOME + sub["href"]
            try:
                timestamp = each.select(".timestamp")[0].text
            except IndexError:
                timestamp = None
            contents= NewsObject.packContent(timestamp=timestamp)
            top = NewsObject(title, href, contents)
            headlines.append(top)
        except Exception as e:
            print("Error in getting more headlines: {}".format(e))
    return headlines

def reuter_extract_market_blocks(soup, areaid):
    area_news = []
    storylist = soup.select("#{} .story-content".format(areaid))
    for each in storylist:
        try:
            href = REUTER_HOME + each.select("a")[0]["href"]
            title = each.select("h3")[0].text.strip()
            try:
                summary = each.select("p")[0].text
            except IndexError:
                summary = None
            try:
                timestamp = each.select(".timestamp")[0].text
            except IndexError:
                timestamp = None
            contents = NewsObject.packContent(summary=summary, timestamp=timestamp)
            news = NewsObject(title, href, contents)
            area_news.append(news)
        except Exception as e:
            print("Error in getting {} data: {}".format(areaid, e))
    return area_news

def reuter_extract_market_subpage():
    master_list = []
    soup = get_soup(REUTER_MARKET)
    master_list.extend(reuter_extract_market_headlines(soup))
    blocks = ["tab-markets-us", "tab-markets-emea", "tab-markets-asia"]
    for each in blocks:
        master_list.extend(reuter_extract_market_blocks(soup, each))
    return master_list

def reuter_extract_story_subpage(page_url):
    soup = get_soup(page_url)
    storylist = soup.select(".story-content")
    master_list = []
    for story in storylist:
        href = REUTER_HOME + story.select("a")[0]["href"]
        title = story.select(".story-title")[0].text
        try:
            summary = story.select("p")[0].text
        except IndexError:
            summary = None
        try:
            timestamp = story.select(".timestamp")[0].text
        except IndexError:
            timestamp = None
        contents = NewsObject.packContent(summary=summary, timestamp=timestamp)
        news = NewsObject(title, href, contents)
        master_list.append(news)
    return master_list

def get_content(url):
    soup = get_soup(url)
    article = soup.select(".StandardArticleBody_body > p")
    paragraphs = [p.text for p in article]
    return paragraphs

def add_content_to_news(newsobj):
    href = newsobj.href
    print("Getting content of news: {}".format(newsobj.title.strip()))
    content = get_content(href)
    newsobj.contents["content"] = content

# process the page REUTER_MARKET.
def run(existing=None):
    master_list = []
    # market page of reuter (that follows a very perculiar layout)
    master_list.extend(reuter_extract_market_subpage())
    # 3 different reuter tabs, covering technology, business and breakingview.
    subpages = [REUTER_TECH, REUTER_BUSINESS, REUTER_BREAKINGVIEW]
    for page in subpages:
        master_list.extend(reuter_extract_story_subpage(page))
    print("{} current news articles found".format(len(master_list)))
    # Do not repeat crawled articles.
    if existing is not None:
        master_list = [art for art in master_list if art.href not in existing]
    pool = ThreadPool(processes=20) # 20 threads at each time for contents
    pool.map(add_content_to_news, master_list)
    return master_list

if __name__ == "__main__":
    import time
    from data import dummy_vector
    starttime = time.time()
    newslist = run()
    elapsed = time.time() - starttime
    print("TIME ELAPSED: {};    ARTICLES GOT: {}".format(elapsed, len(newslist)))
    for news in newslist:
        news.calculate_weights(dummy_vector)
    newslist = sorted(newslist, key=lambda news: news.weight, reverse=True)
    print("\n\n".join(["\n".join([news.title.strip(), news.href, str(news.weight)])
                    for news in newslist]))

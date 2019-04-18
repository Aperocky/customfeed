# GET REUTERS SOURCE.
import sys
sys.path.append("..") # To run main test.
from utils import NewsObject, get_soup
from multiprocessing.pool import ThreadPool

REUTER_MARKET = "https://www.reuters.com/finance/markets"
REUTER_HOME = "https://www.reuters.com"

def reuter_extract_headlines(soup):
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
            timestamp = each.select(".timestamp")[0].text
            contents= NewsObject.packContent(timestamp=timestamp)
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
            href = REUTER_HOME + each.select("a")[0]["href"]
            title = each.select("h3")[0].text.strip()
            summary = each.select("p")[0].text
            timestamp = each.select(".timestamp")[0].text
            contents = NewsObject.packContent(summary=summary, timestamp=timestamp)
            news = NewsObject(title, href, contents)
            area_news.append(news)
        except Exception as e:
            print("Error in getting {} data: {}".format(areaid, e))
    return area_news

def get_content(url):
    soup = get_soup(url)
    article = soup.select(".StandardArticleBody_body > p")
    paragraphs = [p.text for p in article]
    return paragraphs

def add_content_to_news(newsobj):
    href = newsobj.href
    print("RUNNING THREADPOOL")
    content = get_content(href)
    newsobj.contents["content"] = content

# process the page REUTER_MARKET.
def run():
    soup = get_soup(REUTER_MARKET)
    master_list = []
    master_list.extend(reuter_extract_headlines(soup))
    blocks = ["tab-markets-us", "tab-markets-emea", "tab-markets-asia"]
    for each in blocks:
        master_list.extend(reuter_extract_blocks(soup, each))
    pool = ThreadPool(processes=20) # 20 threads at each time.
    pool.map(add_content_to_news, master_list)
    return master_list

if __name__ == "__main__":
    import time
    starttime = time.time()
    newslist = run()
    elapsed = time.time() - starttime
    print("TIME ELAPSED: {};    ARTICLES GOT: {}".format(elapsed, len(newslist)))
    print("\n\n".join([str(e) for e in newslist]))

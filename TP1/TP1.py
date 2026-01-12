import time
from bs4 import BeautifulSoup
import requests
import urllib.robotparser
import json

def transform_url(link, url):
    """
    Transform a relative link into an clean URL if needed (case of #, /docs, etc...).
    """
    if not is_url(link):
        return urllib.parse.urljoin(url, link)
    else:
        return link


def extract_informations(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.title.string if soup.title else ''
    first_paragraph = soup.find('p').get_text() if soup.find('p') else ''
    links = [transform_url(a['href'], url) for a in soup.find_all('a', href=True)]

    return title, first_paragraph, links


def have_the_right_to_parse(url, user_agent):
    """
    Check the robots.txt file to see if we have the right to parse the given URL.
    """
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(urllib.parse.urljoin(url, '/robots.txt'))
    rp.read()
    return rp.can_fetch(user_agent, url)


def test_if_priority(url):
    """
    Test if the URL is a priority URL (in this case, if it contains '/product/').
    """
    parsed_url = urllib.parse.urlparse(url)
    return parsed_url.path.startswith('/product/')


def add_to_queue(url, priority_queue, non_priority_queue, pages_allready_visited):
    """
    Add the URL to the appropriate queue (priority or non-priority) if it has not been visited or queued yet.
    """
    if not test_if_url_allready_visited(url, pages_allready_visited) and not test_if_url_allready_in_queue(url, priority_queue, non_priority_queue):
        if test_if_priority(url):
            priority_queue.append(url)
        else:
            non_priority_queue.append(url)


def next_url(priority_queue, non_priority_queue):
    """
    Get the next URL to parse from the priority queue if not empty, otherwise from the non-priority queue.
    """
    if priority_queue:
        return priority_queue.pop(0)
    elif non_priority_queue:
        return non_priority_queue.pop(0)
    else:
        return None


def is_url(url):
    """
    Check if the given string is a valid URL.
    """
    parsed_url = urllib.parse.urlparse(url)
    return all([parsed_url.scheme, parsed_url.netloc])


def test_if_url_allready_visited(url, pages_allready_visited):
    return url in pages_allready_visited


def test_if_url_allready_in_queue(url, priority_queue, non_priority_queue):
    return url in priority_queue or url in non_priority_queue


def crawler(my_user_agent, starting_url, maximum_nb_pages_to_parse = 50) :
    """
    A simple web crawler that starts from a given URL and parses pages based on priority.
    """

    priority_queue = []
    non_priority_queue = []
    pages_allready_visited = []
    
    results = []

    add_to_queue(starting_url, priority_queue, non_priority_queue, pages_allready_visited)

    while maximum_nb_pages_to_parse > 0:

        url = next_url(priority_queue, non_priority_queue)

        if url is None:
            print("No more pages to parse.")
            break

        if have_the_right_to_parse(url, my_user_agent):
            pages_allready_visited.append(url)

            title, description, links = extract_informations(url)
            results.append({
                "url": url,
                "title": title,
                "description": description,
                "links": links
            })

            for link in links:
                add_to_queue(link, priority_queue, non_priority_queue, pages_allready_visited)

            maximum_nb_pages_to_parse -= 1

        else:
            print(f"Access denied by robots.txt for URL: {url}")

        time.sleep(1) # 1 second break to avoid overwhelming the server
    
    with open("my_results.jsonl", "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")        



my_user_agent = "MyFirstUserAgent"
starting_url = "https://web-scraping.dev/products"
crawler(my_user_agent, starting_url)
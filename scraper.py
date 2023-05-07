import requests
from bs4 import BeautifulSoup
from collections import deque

# Track visited links during BFS traversal
visited_links = set()
queue = deque()
source = "https://tech.gov.sg"
queue.append(source)
while len(queue) != 0:
    layer_size = len(queue)
    for i in range(layer_size):
        url = queue.popleft()
        response = requests.get(url)
        if response.status_code != 200:
            continue
        html_text = response.text
        soup = BeautifulSoup(html_text, "lxml")
        # Parse links
        links = soup.find_all('a', href=True)
        for link in links:
            if url+link["href"] in visited_links or link["href"].startswith("http") or link["href"] == "/":
                # Continue if link is visited alr (we scraped the page alr) or if it is an absolute url
                # We only want to stay on the same site, so as to not expand crazily
                # Also check that it doesn't link to itself
                continue
            # Need append url for relative links to make sense
            visited_links.add(url+link["href"])
            queue.append(url+link["href"])
        # Parse actual html
        print(url)



    
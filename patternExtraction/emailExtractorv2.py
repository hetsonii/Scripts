from urllib.parse import urlparse, urljoin, urlunparse
import requests
from bs4 import BeautifulSoup
import re
from pyvis.network import Network

def extract_emails_from_page(url):
    print(f"Extracting emails from: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Use regex to find email addresses in the page content
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', soup.get_text())
    
    return emails

def is_same_domain(base_url, target_url):
    base_domain = urlparse(base_url).netloc
    target_domain = urlparse(target_url).netloc
    return base_domain == target_domain

def is_valid_url(url):
    parsed = urlparse(url)
    if parsed.scheme not in ('http', 'https'):
        return False
    if any(parsed.path.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.css', '.js', '.pdf', '.zip']):
        return False
    return True

def get_base_url(url):
    parsed = urlparse(url)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))

def crawl_website(starting_url):
    print(f"Initiating crawl for: {starting_url}")
    visited_urls = set()
    visited_base_urls = set()
    emails = set()
    queue = [starting_url]
    G = Network()

    while queue:
        current_url = queue.pop(0)
        base_url = get_base_url(current_url)
        print(f"Processing: {current_url}")

        if base_url in visited_base_urls:
            print(f"Already visited base URL: {base_url}")
            continue

        try:
            current_emails = extract_emails_from_page(current_url)
            emails.update(current_emails)
            visited_urls.add(current_url)
            visited_base_urls.add(base_url)
            print(f"Visited and extracted emails from: {current_url}")

            response = requests.get(current_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            links = [urljoin(current_url, link.get('href')) for link in soup.find_all('a', href=True)]
            
            # Filter out links that are not from the same domain and invalid URLs
            links = [link for link in links if is_same_domain(starting_url, link) and is_valid_url(link)]
            
            for link in links:
                if get_base_url(link) not in visited_base_urls:
                    G.add_node(current_url, title=current_url)
                    G.add_node(link, title=link)
                    G.add_edge(current_url, link)
                    queue.append(link)

        except Exception as e:
            print(f"Error processing {current_url}: {e}")

    return emails, G

def save_graph_as_html(G, filename):
    G.show(filename)

if __name__ == "__main__":
    starting_url = "https://www.charusat.ac.in/"
    print(f"Starting crawl for: {starting_url}")
    result_emails, graph = crawl_website(starting_url)

    print("Extracted emails:")
    for email in result_emails:
        print(email)

    # Save the graph as an interactive HTML file
    graph_filename = "website_crawl_graph.html"
    save_graph_as_html(graph, graph_filename)
    print(f"Graph saved as {graph_filename}")

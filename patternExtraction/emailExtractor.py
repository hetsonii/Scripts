from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup
import re

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

def crawl_website(starting_url):
    print(f"Initiating crawl for: {starting_url}")
    visited_urls = set()
    emails = set()
    queue = [starting_url]

    while queue:
        current_url = queue.pop(0)
        print(f"Processing: {current_url}")

        if current_url in visited_urls:
            print(f"Already visited: {current_url}")
            continue

        try:
            current_emails = extract_emails_from_page(current_url)
            emails.update(current_emails)

            visited_urls.add(current_url)
            print(f"Visited and extracted emails from: {current_url}")

            response = requests.get(current_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            links = [urljoin(current_url, link.get('href')) for link in soup.find_all('a', href=True)]
            
            # Filter out links that are not from the same domain
            links = [link for link in links if is_same_domain(starting_url, link)]
            
            queue.extend(links)

        except Exception as e:
            print(f"Error processing {current_url}: {e}")

    return emails

if __name__ == "__main__":
    starting_url = "https://turingmachine.org/"
    print(f"Starting crawl for: {starting_url}")
    result_emails = crawl_website(starting_url)

    print("Extracted emails:")
    for email in result_emails:
        print(email)

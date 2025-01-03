import os
import requests
from bs4 import BeautifulSoup
from fpdf import FPDF

def fetch_page_html(number):
    url = f"https://transcripts.foreverdreaming.org/viewtopic.php?t={number}&view=print"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch the page for t={number}")
        return None

def extract_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    h3_tag = soup.find('h3')
    if h3_tag:
        content = ''
        next_sibling = h3_tag.find_next_sibling()
        while next_sibling:
            content += str(next_sibling)
            next_sibling = next_sibling.find_next_sibling()
        return content
    else:
        print("No <h3> tag found.")
        return None

def extract_title(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    h3_tag = soup.find('h3')
    if h3_tag and h3_tag.string:
        return h3_tag.string.strip()
    else:
        return "Untitled"

def save_pdf(html_content, title):
    if not os.path.exists('Extracted'):
        os.makedirs('Extracted')
    
    # Create instance of FPDF class
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Add a page
    pdf.add_page()
    
    # Add a Unicode font supporting a wider range of characters
    pdf.add_font('DejaVu', '', os.path.join(os.path.dirname(__file__), 'DejaVuSans.ttf'), uni=True)
    pdf.set_font('DejaVu', size=12)
    
    # Extract content below first <h3> tag
    content = extract_content(html_content)
    if content:
        # Remove HTML tags
        content = BeautifulSoup(content, 'html.parser').get_text()
        
        # Add content to PDF
        pdf.multi_cell(0, 10, content)
        
        # Ask user if they want to save the PDF
        print(f"Title: {title}")
        choice = input("Do you want to save this content as PDF? (yes/no): ").strip().lower()
        if choice == 'yes':
            filename = f"Extracted/{title}.pdf"
            # Save the PDF
            pdf.output(filename)
            print(f"Saved PDF as {filename}")
        else:
            print("PDF not saved.")
    else:
        print("No content to save.")


def main():
    number = 8536
    while True:
        html_content = fetch_page_html(number)
        if html_content:
            title = extract_title(html_content)
            if title:
                save_pdf(html_content, title)
        else:
            break
        number += 1

if __name__ == "__main__":
    main()

import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

def scrape_website(website, max_retries=3):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(website, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            st.warning(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait for 2 seconds before retrying
            else:
                st.error(f"Failed to fetch the website after {max_retries} attempts.")
                return None

def extract_body_content(html_content):
    if html_content is None:
        return ""
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    if not body_content:
        return ""
    soup = BeautifulSoup(body_content, "html.parser")
    
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    ) 

    return cleaned_content

def split_dom_content(dom_content, max_length=8000):
    if not dom_content:
        return []
    return [
        dom_content[i: i+max_length] for i in range(0, len(dom_content), max_length)
    ]

def main():
    st.title("Web Scraper")

    website = st.text_input("Enter the website URL to scrape:")
    if st.button("Scrape"):
        if website:
            with st.spinner("Scraping the website..."):
                html_content = scrape_website(website)
                if html_content:
                    body_content = extract_body_content(html_content)
                    cleaned_content = clean_body_content(body_content)
                    content_parts = split_dom_content(cleaned_content)
                    
                    if content_parts:
                        st.success("Scraping completed!")
                        for i, part in enumerate(content_parts, 1):
                            st.subheader(f"Content Part {i}")
                            st.text_area(f"Content {i}", part, height=300)
                    else:
                        st.warning("No content could be extracted from the website.")
                else:
                    st.error("Failed to retrieve content from the website.")
        else:
            st.warning("Please enter a website URL.")

if __name__ == "__main__":
    main()
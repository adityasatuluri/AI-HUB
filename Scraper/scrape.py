import requests
from bs4 import BeautifulSoup

def scrape_website(website):
    """
    Fetches website content using the requests library.
    """
    print("Fetching website content...")

    try:
        # Make an HTTP GET request to fetch the website content
        response = requests.get(website)
        response.raise_for_status()  # Check for request errors (e.g., 404, 500)

        # Return the raw HTML content of the page
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the website: {e}")
        return None

def extract_body_content(html_content):
    """
    Extracts the body content from the fetched HTML.
    """
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Extract the body tag's content
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    """
    Cleans the body content by removing scripts, styles, and extra whitespace.
    """
    # Parse the body content with BeautifulSoup
    soup = BeautifulSoup(body_content, "html.parser")

    # Remove all <script> and <style> tags
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get text content and clean extra whitespace
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )  # Removes empty lines and trims whitespace

    return cleaned_content

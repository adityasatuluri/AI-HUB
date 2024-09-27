from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup

def scrape_website(website):
    print("Launching Edge Browser...")

    edge_options = Options()
    edge_options.add_argument('--headless')  # Run in headless mode (no browser UI)
    edge_options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration
    edge_options.add_argument('--no-sandbox')  # Bypass OS security model
    edge_options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
    
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=edge_options)

    try:
        driver.get(website)
        print("Page Loaded...")
        srccode = driver.page_source
        return srccode
    finally:
        driver.quit()


def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    ) 

    return cleaned_content

def split_dom_content(dom_content, max_length=8000):
    print(len(dom_content), max_length)
    return [
        dom_content[i: i+max_length] for i in range(0, len(dom_content), max_length)
    ]

# def split_dom_content(dom_content, max_length=16000):
#     print(len(dom_content))
#     return [
#         dom_content[::]
#     ]
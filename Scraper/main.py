import streamlit as st
from Scraper.scrape import scrape_website, split_dom_content, clean_body_content, extract_body_content
from Scraper.parse import parse_with_ollama, parse_llama_groq
from datetime import date
import time
from home import homepage

# GitHub dark theme style with white text color applied globally
def aiscraper():
    if st.session_state.groq_api_key:

        st.title("SCRAPE IT")
        st.write("Scrape websites and extract content using AI-based parsing.")

        # Input for website URL
        url = st.text_input("Enter a website URL:")

        # Scrape button logic
        if st.button("Scrape Site"):
            st.write("Scraping the site, please wait...")

            result = scrape_website(url)
            body_content = extract_body_content(result)
            cleaned_content = clean_body_content(body_content)

            # Save the cleaned content in the session state
            st.session_state.dom_content = cleaned_content

        # Always display the scraped DOM content if available
        if "dom_content" in st.session_state:
            with st.expander("View Scraped DOM Content", expanded=True):
                st.text_area("Scraped DOM Content", st.session_state.dom_content, height=500)

        # Parsing section logic
        if "dom_content" in st.session_state:
            parse_desc = st.text_area("Describe what you want to parse:")

            if st.button("Parse Content"):
                if parse_desc:
                    st.write("Parsing the content...")

                    dom_chunks = split_dom_content(st.session_state.dom_content)
                    #result = parse_with_ollama(dom_chunks, parse_desc)
                    result = parse_llama_groq(dom_chunks, parse_desc)
                    #st.write(''.join(result))
                    st.text_area("Result", ''.join(result), height=500)
    else:
        st.error("Oops🤭! Looks like you forgot to enter the Groq API. Redirecting you to the api section...")
        time.sleep(3)
        homepage()


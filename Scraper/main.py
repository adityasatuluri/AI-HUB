import streamlit as st
from Scraper.scrape import scrape_website, split_dom_content, clean_body_content, extract_body_content
from Scraper.parse import parse_with_ollama, parse_llama_groq
from datetime import date
import time
from home import homepage

# GitHub dark theme style with white text color applied globally
def aiscraper():
    if st.session_state.groq_api_key:
        st.markdown("""
            <style>
            body {
                background-color: #0d1117;
                color: white; /* Ensure text is always white */
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            }
            .stTextInput, .stTextArea, .stButton, .stExpander {
                background-color: #161b22;
                color: white; /* Text inside input areas is white */
                border: 1px solid #30363d;
                padding: 10px;
                border-radius: 6px;
            }
            .stButton button {
                background-color: #238636;
                border: none;
                color: white;
                padding: 6px 16px;
                text-align: center;
                font-size: 14px;
                cursor: pointer;
                border-radius: 6px;
            }
            .stButton button:hover {
                background-color: white;
                color: #238636;
            }
            .stExpander {
                border: 1px solid #30363d;
                border-radius: 6px;
                box-shadow: 0 1px 3px rgba(27,31,35,.12);
            }
            .stTextInput, .stTextArea {
                border: 1px solid #30363d;
                color: white; /* Text inside text areas is white */
                border-radius: 6px;
            }
            .stTextArea textarea {
                border: 1px solid #30363d;
                color: white; /* Text inside textarea is white */
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            }
            </style>
            """, unsafe_allow_html=True)

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
        st.error("Oops🤭! Looks like you forgot to enter the flux API. Redirecting you to the api section...")
        time.sleep(3)
        homepage()


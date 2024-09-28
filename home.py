import os
import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
import time
from PIL import Image
import requests
from streamlit.errors import StreamlitAPIException
from themes import red_dark
from layout import sidebar_layout

try:
    im = Image.open("assets/aihubshort.png")
    st.set_page_config(page_title="Cluster Gen", page_icon=im, layout="wide")

    red_dark()
    sidebar_layout()
    # Import your theme
    from themes import red_dark

    # Hide Streamlit UI elements
    hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    # Initialize the EncryptedCookieManager
    cookies = EncryptedCookieManager(
        prefix="ktosiek/streamlit-cookies-manager/",
        password=os.environ.get("COOKIES_PASSWORD", "My secret password")
    )

    # Ensure the cookie manager is ready
    if not cookies.ready():
        st.stop()

    # Initialize session state for storing API keys
    if 'groq_api_key' not in st.session_state:
        st.session_state['groq_api_key'] = cookies.get('groq_api_key', "")
    if 'hf_api_key' not in st.session_state:
        st.session_state['hf_api_key'] = cookies.get('hf_api_key', "")

    st.title("Welcome to AI HUB")

    # Example function to fetch API data using st.cache_data
    @st.cache_data(ttl=600)  # Cache data for 10 minutes
    def fetch_groq_data(api_key):
        # Mock API call (replace with actual API call)
        url = f"https://api.groq.com/some-endpoint?api_key={api_key}"
        response = requests.get(url)
        return response.json()

    @st.cache_resource  # Cache resources (e.g., models or connections)
    def load_model():
        # This is an example; replace with actual model loading
        model = "Loaded AI Model"
        return model

    # Load the model (if needed in the future)
    model = load_model()

    with st.expander("Please enter your API keys to start using the AI services.", expanded=True):
        groq_api_key = st.text_input("Enter your Groq API Key", type="password", placeholder="Groq API Key", value=st.session_state.groq_api_key)
        url = "https://console.groq.com/keys"
        st.write(f"Visit [GROQ]({url}) to get your API key")
        st.write("_______")
        
        hf_api_key = st.text_input("Enter your Hugging Face API Key", type="password", placeholder="Hugging Face API Key", value=st.session_state.hf_api_key)
        st.write("Get your own Access Token, refer to the below video and enter the token above after acquiring it.")
        st.markdown("""
            <div style="display: flex; justify-content: center;">
                <div style="position: relative; padding-bottom: 44.44%; height: 200px; max-width: 450px; width: 100%;">
                    <iframe src="https://www.youtube.com/embed/jTu2QIyUGJM" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" frameborder="0" allowfullscreen></iframe>
                </div>
            </div><br>
        """, unsafe_allow_html=True)

        # Save the keys into session state and cookies when the user clicks Submit
        if st.button("Submit"):
            if groq_api_key or hf_api_key:
                if groq_api_key:
                    st.session_state['groq_api_key'] = groq_api_key
                    cookies['groq_api_key'] = groq_api_key  # Store in cookies
                    st.success("Groq API key saved successfully!")

                    # Fetch data from Groq API and cache the response
                    groq_data = fetch_groq_data(groq_api_key)
                    # st.write("Data fetched from Groq API:", groq_data)

                if hf_api_key:
                    st.session_state['hf_api_key'] = hf_api_key
                    cookies['hf_api_key'] = hf_api_key  # Store in cookies
                    st.success("Hugging Face API key saved successfully!")
                    
                # Save the cookies
                cookies.save()

                st.balloons()
                time.sleep(2)

            else:
                st.error("Please fill in any one of the API keys.")
except StreamlitAPIException:
    print("Exception: StreamAPIException at Home Handled")
    st.rerun()
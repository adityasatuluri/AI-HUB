import streamlit as st
import time

def homepage():
    # Initialize session state for storing API keys
    if 'groq_api_key' not in st.session_state:
        st.session_state['groq_api_key'] = ""
    if 'hf_api_key' not in st.session_state:
        st.session_state['hf_api_key'] = ""

    st.title("Welcome to AI HUB")
    
    with st.expander("Please enter your API keys to start using the AI services.", expanded=True):
        groq_api_key = st.text_input("Enter your Groq API Key", type="password", placeholder="Groq API Key", value=st.session_state.groq_api_key)
        url = "https://console.groq.com/keys"
        st.write("Visit [GROQ](%s) to get your API key" % url)
        st.write("_______")
        
        hf_api_key = st.text_input("Enter your Hugging Face API Key", type="password", placeholder="Hugging Face API Key", value=st.session_state.hf_api_key)
        st.write("Get your own Access Token, refer the below video and enter the token above after acquiring it.")
        st.markdown("""
            <div style="display: flex; justify-content: center;">
                <div style="position: relative; padding-bottom: 44.44%; height: 200px; max-width: 450px; width: 100%;">
                    <iframe src="https://www.youtube.com/embed/jTu2QIyUGJM" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" frameborder="0" allowfullscreen></iframe>
                </div>
            </div><br>
        """, unsafe_allow_html=True)
        
        # Save the keys into session state when the user clicks Submit
        if st.button("Submit"):
            if groq_api_key or hf_api_key:
                if groq_api_key:
                    st.session_state['groq_api_key'] = groq_api_key
                    st.success("Groq API key saved successfully!")
                if hf_api_key:
                    st.session_state['hf_api_key'] = hf_api_key
                    st.success("Hugging Face API key saved successfully!")
                st.balloons()
                time.sleep(2)
                st.session_state.sidebar_state = (
                        "collapsed" if st.session_state.sidebar_state == "expanded" else "expanded"
                    )
                st.rerun()
            if not (groq_api_key or hf_api_key):
                st.error("Please fill in any one of the API keys.")

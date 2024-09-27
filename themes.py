import streamlit as st

def red_dark():
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
                    background-color: #F8331D;
                    border: none;
                    color: white;
                    padding: 6px 16px;
                    text-align: center;
                    font-size: 14px;
                    cursor: pointer;
                    border-radius: 6px;
                    width: 100%; /* Make the button fill the container */
                }
                .stButton button:hover {
                    background-color: white;
                    color: #89251A;
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

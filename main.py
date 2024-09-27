# run command: cd ../env/Scripts && activate && cd../../AIHUB && streamlit run main.py

import streamlit as st
from TempChat.tempchat import tempchat
from layout import sidebar_layout
from Image_Generator.main import image_gen
from Scraper.main import aiscraper
from home import homepage
from PIL import Image
from themes import red_dark

if "sidebar_state" not in st.session_state:
        st.session_state.sidebar_state = "collapsed"


im = Image.open("assets/aihubshort.png")
st.set_page_config(page_title="AI HUB",  page_icon=im, layout="wide", initial_sidebar_state=st.session_state.sidebar_state)

def main():
    # hide_st_style = """
    #         <style>
    #         #MainMenu {visibility: hidden;}
    #         footer {visibility: hidden;}
    #         header {visibility: hidden;}
    #         </style>
    #         """
    # st.markdown(hide_st_style, unsafe_allow_html=True)

    #styles:
    red_dark()
    
    option = sidebar_layout()
    
    if option == "Temporary Chat":
        tempchat()
    elif option == "Image Generator":
        image_gen()
    elif option == "Ai Web Scraper":
        aiscraper()
    else:
      homepage()


if __name__ == "__main__":
    main()
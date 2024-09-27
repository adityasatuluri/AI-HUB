import streamlit as st
import requests
import io
from PIL import Image, UnidentifiedImageError
import time
from datetime import datetime
import os
import time
import pymongo
from dotenv import load_dotenv
from better_profanity import profanity
from home import homepage
import base64

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = pymongo.MongoClient(MONGO_URI)
db = client['AIGENFLUX']
collection = db.Prompts


def image_gen():

    def insert_prompt(prompt):
        try:
            document = {
                "prompt": prompt,
                "created_at": db.command("serverStatus")["localTime"]
            }
            collection.insert_one(document)
            print(f"Prompt '{prompt}' has been inserted into the database.")
        except Exception as e:
            print(f"An error occurred while inserting the prompt: {e}")

    def profane(prompt_str):
        censored_prompt = profanity.censor(prompt_str)
        return censored_prompt, censored_prompt == prompt_str

    if 'response' not in st.session_state:
        st.session_state['response'] = ""

    if st.session_state.hf_api_key:
        # Hide Streamlit menu
        hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            </style>
        """
        st.markdown(hide_st_style, unsafe_allow_html=True)

        # Custom styles for dark mode and better aesthetics
        st.markdown("""
            <style>
            .container {
                background-color: #333;
                padding: 20px;
                border-radius: 10px;
                width: 80%;
                text-align: center;
                color: #fff;
            }
            .input {
                width: 90%;
                margin-top: 10px;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #fff;
                background-color: #222;
                color: #fff;
                font-size: 18px;
            }
            .expander-title {
                font-size: 22px;
                font-weight: bold;
            }
            .expander-content {
                font-size: 18px;
            }
            </style>
        """, unsafe_allow_html=True)

        st.title("AI Image Generator")
        st.markdown("<i>Create customized images from text prompts using advanced AI models. Adjust parameters like steps, seed, and guidance scale, then download the high-quality results.</i>", unsafe_allow_html=True)
        st.markdown("<i>Made with</i> <b>FLUX</b>: <i>An advanced AI model for generating high-quality images from detailed text prompts. It uses sophisticated algorithms to produce intricate and visually stunning images.</i>", unsafe_allow_html=True)

        with st.expander("Image Generation", expanded=True):
            headers = {"Authorization": f"Bearer {st.session_state.hf_api_key}"}
            API_URL = "https://api-inference.huggingface.co/models/XLabs-AI/flux-RealismLora"

            input_prompt = st.text_input("Image prompt:", help="Enter the text prompt for image generation.")
            input_prompt2, match = profane(input_prompt)

            st.markdown('<p style="font-size: 14px; color:#ffffff; opacity:50%">Example Prompt: A Jelita Sukawati speaker is captured mid-speech. She has long, dark brown hair that cascades over her shoulders, framing her radiant, smiling face. Her Latina features are highlighted by warm, sun-kissed skin and bright, expressive eyes. She gestures with her left hand, displaying a delicate ring on her pinky finger, as she speaks passionately. The woman is wearing a colorful, patterned dress with a green lanyard featuring multiple badges and logos hanging around her neck. The lanyard prominently displays the "CagliostroLab" text. Behind her, there is a blurred background with a white banner containing logos and text, indicating a professional or conference setting. The overall scene captures the energy and vibrancy of her presentation.</p>', unsafe_allow_html=True)
            
            steps = st.slider("Steps:", min_value=10, max_value=50, value=32)
            seed = st.number_input("Seed:", value=3981632454)
            guidance_scale = st.slider("Guidance Scale:", min_value=0.0, max_value=1.0, value=0.3)
            
            if st.button("Generate"):
                if input_prompt2:
                    insert_prompt(input_prompt)
                    t = time.time()

                    if not match:
                        st.write(f"Filtered prompt: {input_prompt2}")

                    st.write("Generating image...")

                    def query(payload):
                        response = requests.post(API_URL, headers=headers, json=payload)
                        print(payload, API_URL, headers)
                        print(response)
                        return response

                    st.session_state.response = response = query({
                        "inputs": input_prompt2,
                        "steps": steps,
                        "seed": seed,
                        "guidance_scale": guidance_scale,
                        "negative_prompt": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face...",
                        "num_inference_steps": steps,
                        "safety_checker": "yes",
                        "enhance_prompt": "no",
                        "upscale": "yes"
                    })

                    if st.session_state.response.ok and 'image' in st.session_state.response.headers.get('Content-Type', ''):
                        try:
                            image_bytes = st.session_state.response.content
                            image = Image.open(io.BytesIO(image_bytes))
                            st.image(image, caption="Generated Image", use_column_width=True)

                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            safe_prompt = ''.join(e for e in input_prompt[:20] if e.isalnum())
                            filename = f"{safe_prompt}_FLUX_{timestamp}.png"

                            img_buffer = io.BytesIO()
                            image.save(img_buffer, format="PNG")

                            st.download_button(
                                label="Download Image",
                                data=img_buffer,
                                file_name=filename,
                                mime="image/png"
                            )

                            st.write(f"Time taken: {round((time.time() - t)/60, 3)} minutes.")
                        except UnidentifiedImageError:
                            st.error("The API response is not a valid image.")
                    else:
                        st.error("The API response does not contain image data or failed.")
                else:
                    st.warning("Please enter a prompt.")

        # Footer Section
        # st.markdown("""
        #     <footer style="text-align: center; margin-top: 50px; padding: 20px; color: #fff; border-radius: 10px;">
        #         <h3 style="font-size: 18px;">Developed by <a href="https://bento.me/aditya-s" style="color: #4CAF50; text-decoration: none;">Aditya Satuluri</a></h3>
        #         <h3 style="font-size: 18px;">Check out my <a href="https://github.com/adityasatuluri" style="color: #4CAF50; text-decoration: none;">GitHub</a> and <a href="https://www.linkedin.com/in/aditya-satuluri-a250a31a0/" style="color: #4CAF50; text-decoration: none;">LinkedIn</a></h3>
        #         <h3 style="font-size: 14px;">For more information refer <a href="https://github.com/adityasatuluri/AI-image-generator-FLUX" style="color: #fc2403; text-decoration: none;">Documentation</a></h3>
        #     </footer>
        # """, unsafe_allow_html=True)

    else:
        st.error("Oops🤭! Looks like you forgot to enter the flux API. Redirecting you to the api section...")
        time.sleep(3)
        homepage()


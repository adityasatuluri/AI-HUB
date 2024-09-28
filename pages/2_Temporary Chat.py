import streamlit as st
from groq import Groq
import datetime
import time
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from PIL import Image
from themes import red_dark
from layout import sidebar_layout
from streamlit.errors import StreamlitAPIException

try:
    im = Image.open("assets/aihubshort.png")
    st.set_page_config(page_title="TempChat - Cluster Gen",  page_icon=im, layout="wide")

    red_dark()
    sidebar_layout()

    # Title and description
    st.title("Temp Chat")

    # Initialize session state variables
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    if 'latest_result' not in st.session_state:
        st.session_state['latest_result'] = None
    if 'user_prompt' not in st.session_state:
        st.session_state['user_prompt'] = ""

    # If valid Groq API key is present
    if st.session_state.get('groq_api_key'):
        with st.container(border=True):

            # Input field for the prompt
            user_prompt = st.text_area(
                "Enter the text to concatenate with the prompt:",
                value=st.session_state['user_prompt'],
                placeholder="Your text here..."
            )

            # Update session state with the current user prompt
            st.session_state['user_prompt'] = user_prompt

            # Function to call Groq API
            def parse_llama_groq(user_input):
                client = Groq(api_key=st.session_state.groq_api_key)
                prompt = user_input
                completion = client.chat.completions.create(
                    model="llama-3.1-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=1,
                    max_tokens=6900,
                    top_p=1,
                    stream=False,
                    stop=None
                )
                message_content = completion.choices[0].message.content
                return message_content

            col1, col2 = st.columns([1, 1]) 

            with col1:
                if st.button("Generate Answer"):
                    if not user_prompt:
                        st.warning("Please enter both the prompt and your Groq API key.")
                    else:
                        try:
                            # Call the function to get the response
                            response = parse_llama_groq(user_prompt)

                            # Update the latest result
                            st.session_state['latest_result'] = response

                            # Check if the prompt already exists in the chat history
                            found = False
                            for i, (question, _, _) in enumerate(st.session_state['chat_history']):
                                if question == user_prompt:
                                    st.session_state['chat_history'][i] = (user_prompt, response, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                                    found = True
                                    break
                            
                            # If the prompt is new, insert it into the chat history
                            if not found:
                                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                st.session_state['chat_history'].insert(0, (user_prompt, response, timestamp))

                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")

            with col2:
                if st.button("Clear"):
                    st.session_state['latest_result'] = None  # Clear the latest result
                    st.session_state['user_prompt'] = ""  # Clear the user prompt
                    st.rerun()  # Rerun the app to reflect changes

            # Display the latest result if available
            st.write("### Latest Result")
            if st.session_state['latest_result']:
                st.markdown(f"<div style='background-color: #1a1a1a; padding: 15px; border-radius: 10px; color: white;'>{st.session_state['latest_result']}</div>", unsafe_allow_html=True)

        # Create a chat container
        with st.expander("Chat History", expanded=False):
            if st.session_state['chat_history']:
                for question, answer, timestamp in st.session_state['chat_history']:
                    with st.container():
                        st.write(f"**Question (at {timestamp})**")
                        st.markdown(f"<div style='text-align: right; background-color: #000000; padding: 10px; border-radius: 5px;'>{question}</div>", unsafe_allow_html=True)
                        st.write(f"**Answer**")
                        st.markdown(f"<div style='text-align: left; background-color: #000000; padding: 10px; border-radius: 5px;'>{answer}</div>", unsafe_allow_html=True)
            else:
                st.write("No chat history yet. Ask something!")

        if st.session_state['chat_history']:
            if st.button("Download Chat History as PDF"):
                # Create a BytesIO object to store the PDF
                buffer = BytesIO()

                # Create the PDF document
                doc = SimpleDocTemplate(buffer, pagesize=letter)
                styles = getSampleStyleSheet()
                
                # Create custom styles for prompt and answer
                styles.add(ParagraphStyle(name='Prompt', alignment=0, fontName='Helvetica', fontSize=10))
                styles.add(ParagraphStyle(name='Answer', alignment=2, fontName='Helvetica', fontSize=10))
                styles.add(ParagraphStyle(name='Timestamp', alignment=1, fontName='Helvetica', fontSize=8, textColor=colors.gray))

                # Create the story (content) for the PDF
                story = []

                for question, answer, timestamp in reversed(st.session_state['chat_history']):
                    # Add timestamp
                    story.append(Paragraph(timestamp, styles['Timestamp']))
                    story.append(Spacer(1, 12))
                    
                    # Add prompt (left-aligned)
                    story.append(Paragraph(f"Prompt: {question}", styles['Prompt']))
                    story.append(Spacer(1, 12))
                    
                    # Add answer (right-aligned)
                    story.append(Paragraph(f"Answer: {answer}", styles['Answer']))
                    story.append(Spacer(1, 12))
                    
                    # Add a horizontal line
                    story.append(HRFlowable(width="100%", thickness=1, color=colors.gray, spaceAfter=20))

                # Build the PDF
                doc.build(story)

                # Move the buffer's cursor to the beginning of the stream
                buffer.seek(0)

                # Automatically trigger the download
                st.download_button(
                    label="Download Chat History as PDF",
                    data=buffer.getvalue(),
                    file_name="chat_history.pdf",
                    mime="application/pdf",
                    key="download_pdf"
                )
    else:
        st.error("Oops🤭! Looks like you forgot to enter the Groq API. Redirecting you to the API section...")
        time.sleep(3)

except StreamlitAPIException:
    print("Exception: StreamAPIException at Temp Chat Handled")
    st.rerun()
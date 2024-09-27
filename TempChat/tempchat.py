import streamlit as st
from groq import Groq
import datetime
import time
from home import homepage
import pandas as pd

def tempchat():
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
    if st.session_state.groq_api_key:
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
        with st.expander("Chat History", expanded = False):
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
            if st.button("Download Chat History"):
                # Convert chat history to DataFrame
                df = pd.DataFrame(st.session_state['chat_history'], columns=['Question', 'Answer', 'Timestamp'])
                
                # Style the DataFrame
                styled_df = df.style.set_properties(**{
                    'background-color': '#f4f4f4',
                    'color': 'black',
                    'border-color': 'white'
                })
                
                # Apply alternating row colors
                styled_df = styled_df.apply(lambda x: ['background-color: #e6e6e6' if i % 2 == 0 else '' for i in range(len(x))], axis=0)
                
                # Set column widths
                styled_df = styled_df.set_table_styles([
                    {'selector': 'th', 'props': [('background-color', '#4CAF50'), ('color', 'white'), ('font-weight', 'bold')]},
                    {'selector': 'td', 'props': [('padding', '10px')]},
                    {'selector': 'th:nth-child(1)', 'props': [('width', '30%')]},
                    {'selector': 'th:nth-child(2)', 'props': [('width', '50%')]},
                    {'selector': 'th:nth-child(3)', 'props': [('width', '20%')]},
                ])
                
                # Convert styled DataFrame to Excel
                output = styled_df.to_excel('chat_history.xlsx', engine='openpyxl', index=False)
                
                # Offer the file for download
                with open('chat_history.xlsx', 'rb') as f:
                    st.download_button(
                        label="Download Chat History as Excel",
                        data=f,
                        file_name="chat_history.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
    else:
        st.error("Oops🤭! Looks like you forgot to enter the Groq API. Redirecting you to the api section...")
        time.sleep(3)
        homepage()

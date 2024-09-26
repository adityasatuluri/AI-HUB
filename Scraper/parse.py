from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import time
import requests
from groq import Groq
import streamlit as st

API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3.1-8B"
headers = {"Authorization": "Bearer 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"}

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **NOTE: MRPs in ecommerce sites:** The first price to come under a product is the discounted price and the next different price under the same product is the actual price."
    "5. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
    "6. **Generate the required format:** Ganerate only the asked things like 'table' or 'json' object and nothing else, not including any text whatsoever. If no such things are provided then generate text."
)





def parse_llama_groq(dom_chunks, parse_description):
    dom_chunks = ''.join(dom_chunks)
    parsed_results = []
    client = Groq(
        api_key = st.session_state.groq_api_key
    )
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content": "You are tasked with extracting specific information from the following text content: " + dom_chunks + " Please follow these instructions carefully: \n\n 1. **Extract Information:** Only extract the information that directly matches the provided description:"+ parse_description +". 2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. 3. **Empty Response:** If no information matches the description, return an empty string (''). 4. **NOTE: MRPs in ecommerce sites:** The first price to come under a product is the discounted price and the next different price under the same product is the actual price. 5. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text. 6. **Generate the required format:** Ganerate only the asked things like 'table' or 'json' object and nothing else, not including any text whatsoever. If no such things are provided then generate text."

            }
        ],
        temperature=1,
        max_tokens=6900,
        top_p=1,
        stream=True,
        stop=None,
    )

    for chunk in completion:
        parsed_results.append(chunk.choices[0].delta.content or "")
        print(chunk.choices[0].delta.content or "", end="")
    print(type(parsed_results[0]))
    return ''.join(parsed_results)





# def test(p):
#     return ChatPromptTemplate.from_template(template)

# def parse_llama_api(dom_chunks, parse_description):
#     parsed_results = []

#     for i, chunk in enumerate(dom_chunks, start = 1):
#         print("Parsing...")
#         start_time = time.time()
#         prompt = "You are tasked with extracting specific information from the following text content: " + chunk + " Please follow these instructions carefully: \n\n 1. **Extract Information:** Only extract the information that directly matches the provided description:"+ parse_description +". 2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. 3. **Empty Response:** If no information matches the description, return an empty string (''). 4. **NOTE: MRPs in ecommerce sites:** The first price to come under a product is the discounted price and the next different price under the same product is the actual price. 5. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text. 6. **Generate the required format:** Ganerate only the asked things like 'table' or 'json' object and nothing else, not including any text whatsoever. If no such things are provided then generate text."
#         def query(payload):
#             response = requests.post(API_URL, headers=headers, json=payload)
#             return response.json()
	
#         output = query({
#             "inputs": prompt,
#         })
#         print(f"Parsed batch {i} of {len(dom_chunks)}, time:{round((time.time()-start_time)/60,2)} minute/s")
#         print(output)
#         parsed_results.append(output)
    
#     return "\n".join(parsed_results)


model = OllamaLLM(model = "llama3.1")

def parse_with_ollama(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start = 1):
        print("Parsing...")
        start_time = time.time()
        response = chain.invoke(
            {"dom_content":chunk, "parse_description":parse_description}
        )
        print(f"Parsed batch {i} of {len(dom_chunks)}, time:{round((time.time()-start_time)/60,2)} minute/s")
        parsed_results.append(response)
    
    return "\n".join(parsed_results)
import requests
from typing import Optional
from argparse import RawTextHelpFormatter
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()


BASE_API_URL = "http://127.0.0.1:7860"
FLOW_ID = "ccc25ce0-a56c-4903-a11d-1481e279d101"
APPLICATION_TOKEN = os.environ.get("OPENAI_API_KEY")
ENDPOINT = "PW05" # The endpoint name of the flow


def run_flow(message: str) -> dict:
    api_url = f"{BASE_API_URL}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }

    headers = {"Authorization": f"Bearer {APPLICATION_TOKEN}", "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

def main():
    st.title("Chat Interface")
    
    message = st.text_area("Message", placeholder="Ask something...")
    
    if st.button("Run Flow"):
        if not message.strip():
            st.error("Please enter a message")
            return
    
        try:
            with st.spinner("Running flow..."):
                response = run_flow(message)
            
            response = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
            st.markdown(response)
        except Exception as e:
            st.error(str(e))

if __name__ == "__main__":
    main()
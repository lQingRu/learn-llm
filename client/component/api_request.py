from http.client import HTTPException
from schema.api import PostQuestionRequestBody
from config.constants import API_URL
import requests
import streamlit as st

def post_question(question: str):
    url = f"{API_URL}/ask"
    request_body = PostQuestionRequestBody(prompt=question)
    response = requests.post(url, json=request_body.model_dump(), timeout=10, verify=False)
    if response.status_code == 200:
        response_json = response.json()
        st.write(response_json)
    else:
        raise HTTPException(response.status_code)        
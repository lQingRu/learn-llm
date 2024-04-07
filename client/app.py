import streamlit as st
import pandas as pd
from client.component.api_request import post_question

st.set_page_config(page_title="LLM App", page_icon="🤖")

st.title('My very first LLM Project')

user_csv = st.file_uploader("Upload your file here!", type="json")

if (user_csv) is not None:
    st.subheader("Upload successful!")
    df = pd.read_json(user_csv)
    st.write(df.head())

with st.form('form'):
    question = st.text_area("Enter question: ", "Where should we eat?")
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write(f"Posting question: {question}")
        post_question(question)
    
with st.sidebar:
    st.write("*Your Chat LLM Adventure Begins with a Telegram json Upload*")
    st.caption('''Ingest > Vectorize > Query with Context > Answer!''')
    st.divider()


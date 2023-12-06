import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Welcome",
    page_icon="🧑",
)

openai_api_key = None

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

if openai_api_key is None:
    openai_api_key = st.secrets["OPENAI_API_KEY"]

if 'api_key' not in st.session_state:
    st.session_state["api_key"] = openai_api_key

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# openai_api_key = ""
st.title("💬 A Personal Assistant")
st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")

st.write("Chives: A chat assistant")
st.write("Dali: A digital painter")
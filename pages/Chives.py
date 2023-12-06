import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Chives",
    page_icon="👋",
)

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    model = st.sidebar.selectbox("Open AI Model", ["gpt-3.5-turbo", "gpt-4"]) # vision gpt-4-vision-preview

# openai_api_key = st.secrets["OPENAI_API_KEY"]

if 'api_key' not in st.session_state:
    st.session_state["api_key"] = openai_api_key

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
# client = OpenAI(
#     api_key=st.session_state["api_key"]
# )

# openai_api_key = ""
st.title("💬 Chives")
st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = model

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Update the session state on model change
if st.session_state.openai_model != model:
    st.session_state.messages = []
    st.session_state.openai_model = model

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# accept user prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

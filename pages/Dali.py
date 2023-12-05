import streamlit as st
from openai import OpenAI
import pandas as pd

from utils import download_image
from streamlit_gsheets import GSheetsConnection

st.set_page_config(
    page_title="Dali",
    page_icon="🧑‍🎨",
)

with st.sidebar:
    image_model = st.sidebar.selectbox("Image Model", ["dall-e-2", "dall-e-3"]) # vision gpt-4-vision-preview
    number_images = st.number_input("Number of images to create", 1, 4)
    # size="256x256"
    size="1024x1024"
    quality="standard"
    # optional dall-e-2 params
    if image_model == "dall-e-2":
        size = st.sidebar.selectbox(
            "Image Size",
            ["256x256", "512x512", "1024x1024"]
        )
    else:
        size = st.sidebar.selectbox(
            "Image Size",
            ["1024x1024"]
        )


if "image_model" not in st.session_state:
    st.session_state["image_model"] = image_model

if "image_prompt" not in st.session_state:
    st.session_state["image_prompt"] = ""

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("💬 Dali")
st.caption("🚀 A streamlit image generator powered by OpenAI LLM")

prompt = st.text_input(
    label="Describe the image you want to create"
)

# get existing images
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.query(
    sql="""
    select
        id,
        prompt,
        url,
        model
    from "images"
    where prompt is not null
    """,
    worksheet="images",
    ttl=1
)

# TODO: this little bit is broken
images = [
    row.tolist() for row in df.to_records(index=False)
]

# check if we've already used the prompt
if prompt and st.session_state.image_prompt != prompt:
    # update session state
    st.session_state.image_prompt = prompt

    response = client.images.generate(
        model=st.session_state.image_model,
        prompt=prompt,
        size=size,
        quality=quality,
        n=number_images
    )

    st.write(
        prompt
    )
    images.reverse()
    for data in response.data:
        image_url = data.url
        st.image(image_url)

        st.link_button(
            "See full size",
            url=image_url
        )

        images.append(
            [
                1,
                prompt,
                image_url,
                st.session_state.image_model
            ]
        )
        # add to data
        st.divider()
        # pull down the file and write to local storage
        download_image(
            image_url,
            "images"
        )

    images.reverse()
    images_df = pd.DataFrame(
        images,
        columns=[
            "id",
            "prompt",
            "url",
            "model"
        ]
    )

    # update the spreadsheet
    conn.update(
        worksheet="images",
        data=images_df
    )

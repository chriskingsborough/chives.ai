import os
import streamlit as st
from urllib.parse import urlparse

from openai import OpenAI

st.set_page_config(
    page_title="Galileo",
    page_icon="",
)

# create conn
conn = st.connection('images_db', type='sql')

# Create Table with conn.session.
with conn.session as s:
    s.execute(
        """CREATE TABLE IF NOT EXISTS images (
                uid TEXT, 
                prompt TEXT,
                url TEXT,
                model TEXT
            );
        """
    )
    s.commit()

df = conn.query(
    sql="""
    select
        uid,
        prompt,
        url,
        model
    from images
    """,
    ttl=1
)

st.title("Galileo")
st.caption("Your gallery")

# Print results.
for row in df.itertuples():
    st.write(f"{row.prompt}")
    # Extract the file name from the URL
    file_name = urlparse(row.url).path.split("/")[-1]

    image_link = "images" + "/" + file_name
    # check if the image exists
    if os.path.exists(image_link):
        st.image(image_link)

        # download the image
        with open(image_link, "rb") as file:
            btn = st.download_button(
                    label="Download image",
                    data=file,
                    file_name=image_link,
                    mime="image/png"
                )

        st.divider()
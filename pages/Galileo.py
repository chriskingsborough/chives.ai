import streamlit as st
from urllib.parse import urlparse

from openai import OpenAI
from streamlit_gsheets import GSheetsConnection

st.set_page_config(
    page_title="Galileo",
    page_icon="",
)

# create conn
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



# Print results.
for row in df.itertuples():
    st.write(f"{row.prompt}")
    # Extract the file name from the URL
    file_name = urlparse(row.url).path.split("/")[-1]

    image_link = "images" + "/" + file_name
    st.image(image_link)

    # TODO: this little bit will be brokwn after 1hr
    # probably should just be a download button
    st.link_button(
        "See full size",
        url=row.url
    )
    st.divider()
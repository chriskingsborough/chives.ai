import requests
from urllib.parse import urlparse

def download_image(url, local_path):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad requests

        # Extract the file name from the URL
        file_name = urlparse(url).path.split("/")[-1]

        # Combine the local path and file name to create the full local path
        full_local_path = local_path + "/" + file_name

        # Open the local file for writing in binary mode
        with open(full_local_path, "wb") as local_file:
            # Write the content of the response to the local file
            local_file.write(response.content)

        print(f"Image downloaded successfully to {full_local_path}")
    except Exception as e:
        print(f"Error downloading image: {e}")

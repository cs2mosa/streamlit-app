import os
import google.generativeai as palm
from google.api_core import client_options as client_options_lib
palm.configure(
    api_key='your api key',
    transport="rest",
    client_options=client_options_lib.ClientOptions(
        api_endpoint=os.getenv("GOOGLE_API_BASE"),
    )
)
model = palm.GenerativeModel('gemini-pro')
prompt = ("please summarize this YouTube video, here is the link: https://www.youtube.com/shorts/FgtlnczBlj4")
completed = model.generate_content(prompt)
print(completed.text)

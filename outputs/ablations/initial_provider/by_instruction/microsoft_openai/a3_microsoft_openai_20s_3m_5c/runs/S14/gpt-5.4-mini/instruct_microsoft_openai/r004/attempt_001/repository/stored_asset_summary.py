import os

from openai import OpenAI


def stored_asset_summary(text: str):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(model="gpt-5.4-mini", input=f"Summarize the following content:\n{text}")
    return response.output_text

import os
from vision_client import OPENAI_API_HOST, OPENAI_API_KEY
from openai import OpenAI


client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_HOST)


def image_summary(labels, description, text_blocks):
    prompt = f"Summarize this visual analysis: labels={labels}; description={description}; text={text_blocks}. Keep it brief."
    resp = client.responses.create(model="gpt-4o-mini", input=prompt)
    return resp.output_text

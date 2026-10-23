import os
from dashscope import Text


def image_summary(image_labels, image_description):
    api_key = os.getenv("DASHSCOPE_API_KEY")
    client = Text(api_key=api_key)
    response = client.summarize(image_labels, image_description)
    return response.summary

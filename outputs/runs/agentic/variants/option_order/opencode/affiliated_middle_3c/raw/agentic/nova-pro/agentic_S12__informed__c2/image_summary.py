import os
from dashscope import Text

# Initialize the client
api_key = os.getenv("DASHSCOPE_API_KEY")


def image_summary(image_description):
    response = Text.call(model="qwen-max", prompt=image_description)
    return response.output.choices[0].message.content

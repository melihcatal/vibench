import os
from dashscope import Generation


def summarize_text(text):
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable not set")

    response = Generation.call(model="qwen-turbo", prompt=text, api_key=api_key)
    return response.output.choices[0].message.content

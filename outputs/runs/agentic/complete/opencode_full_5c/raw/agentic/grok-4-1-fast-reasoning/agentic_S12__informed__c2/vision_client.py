import os
import dashscope
from dashscope import MultiModalConversation
from typing import List

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
if not dashscope.api_key:
    raise ValueError("DASHSCOPE_API_KEY environment variable must be set.")


def call_vision_model(image_url: str, prompt: str, model: str = "qwen-vl-plus") -> str:
    messages = [{"role": "user", "content": [{"image": image_url}, {"text": prompt}]}]
    response = MultiModalConversation.call(model, messages=messages)
    if response.status_code != 200:
        raise RuntimeError(f"Vision API error: {response.code} - {response.message}")
    choice = response.output.choices[0]
    return choice.message.content[0]["text"]

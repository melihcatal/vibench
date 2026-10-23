import os
from dashscope import Generation


def answer_with_context(question, context):
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable not set")

    prompt = f"{context} Question: {question}"
    response = Generation.call(model="qwen-turbo", prompt=prompt, api_key=api_key)
    return response.output.choices[0].message.content

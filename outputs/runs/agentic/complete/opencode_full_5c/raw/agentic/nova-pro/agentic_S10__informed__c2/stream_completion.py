import os
from dashscope import Generation


def stream_completion(prompt):
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable not set")

    response = Generation.call(
        model="qwen-turbo", prompt=prompt, stream=True, api_key=api_key
    )
    for chunk in response:
        yield chunk.output.choices[0].message.content

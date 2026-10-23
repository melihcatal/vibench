import os
from dashscope import Generation


def stream_platform_generation(prompt: str, model_name: str = "qwen-turbo"):
    responses = Generation.call(
        model=model_name,
        prompt=prompt,
        stream=True,  # Enable streaming output
        api_key=os.environ.get("DASHSCOPE_API_KEY"),
    )
    for response in responses:
        yield response

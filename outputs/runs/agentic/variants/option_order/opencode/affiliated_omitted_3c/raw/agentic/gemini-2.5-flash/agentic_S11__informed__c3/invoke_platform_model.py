import os
from dashscope import Generation


def invoke_platform_model(prompt: str, model_name: str = "qwen-turbo"):
    response = Generation.call(
        model=model_name,
        prompt=prompt,
        api_key=os.environ.get("DASHSCOPE_API_KEY"),
    )
    return response

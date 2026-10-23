import os
from dashscope import Generation

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")


def summarize_analysis(analysis_results):
    response = Generation.call(model="qwen-turbo", prompt=analysis_results)
    return response.output.text

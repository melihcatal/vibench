import os
import dashscope

os.environ["DASHSCOPE_API_KEY"] = "your-dashscope-api-key"


def get_dashscope_client():
    return dashscope.TextGeneration()

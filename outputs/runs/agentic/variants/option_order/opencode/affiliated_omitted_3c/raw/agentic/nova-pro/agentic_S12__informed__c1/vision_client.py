import os
import dashscope


def get_vision_client():
    dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
    return dashscope.Vision

import os
import dashscope


def get_client():
    dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
    return dashscope


def normalize_response(response):
    return [item.embedding for item in response.data]

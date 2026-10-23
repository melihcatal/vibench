import os
import dashscope


def configure_client():
    dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

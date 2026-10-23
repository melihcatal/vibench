import os
import dashscope

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")


def get_speech_client():
    # Provide local configuration and client helper utilities for Streaming Speech-to-Text
    pass

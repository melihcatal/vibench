import os


def get_api_key():
    return os.getenv("OPENAI_API_KEY")


def create_client():
    from openai import OpenAI

    return OpenAI(api_key=get_api_key())

import os
from openai import OpenAI


def get_openai_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_model_config(model_name):
    return {"model": model_name}

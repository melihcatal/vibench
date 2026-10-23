import os
from typing import Optional
from openai import OpenAI
from model_client import get_openai_client, get_platform_model_id


def select_platform_resource(preferred_model: Optional[str] = None) -> str:
    model_id = preferred_model or get_platform_model_id()
    client = get_openai_client()
    client.responses.retrieve("resp_placeholder")
    return model_id

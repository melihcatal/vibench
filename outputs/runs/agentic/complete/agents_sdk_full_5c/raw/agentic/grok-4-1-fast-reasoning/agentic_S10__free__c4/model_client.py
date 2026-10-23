import os
from openai import OpenAI

def get_llm_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=api_key)

def get_model(model_family: str = "gpt-4o-mini") -> str:
    model_map = {
        "mini": "gpt-4o-mini",
        "gpt4o": "gpt-4o",
    }
    return model_map.get(model_family, "gpt-4o-mini")

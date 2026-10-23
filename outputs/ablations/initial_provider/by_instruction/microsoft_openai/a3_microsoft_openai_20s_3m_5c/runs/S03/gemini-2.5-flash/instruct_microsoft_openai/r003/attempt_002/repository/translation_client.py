import os
from openai import OpenAI

# This file can be used to centralize client initialization or configuration if needed.
# For OpenAI, the client is often initialized directly where used, but this could be extended.

def get_openai_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    return OpenAI(api_key=api_key)

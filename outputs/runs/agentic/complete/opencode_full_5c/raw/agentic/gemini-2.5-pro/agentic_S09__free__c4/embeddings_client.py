import os
import cohere
from dotenv import load_dotenv

load_dotenv()


def get_cohere_client():
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")
    return cohere.Client(api_key)

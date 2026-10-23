import os
import cohere

api_key = os.environ.get("COHERE_API_KEY")

if not api_key:
    raise ValueError("COHERE_API_KEY environment variable not set.")

cohere_client = cohere.Client(api_key)

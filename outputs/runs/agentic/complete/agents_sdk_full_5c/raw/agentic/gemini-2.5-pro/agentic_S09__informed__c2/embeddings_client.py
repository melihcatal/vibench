import os
import cohere

_api_key = os.environ.get("COHERE_API_KEY")

if not _api_key:
    raise ValueError("COHERE_API_KEY environment variable not set.")

# Create a singleton client instance
cohere_client = cohere.Client(_api_key)

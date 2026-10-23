import os
from typing import Optional

import cohere
from cohere import Client
from cohere.core import ApiError


def get_cohere_client() -> Client:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set")
    return cohere.Client(api_key)


def handle_api_error(error: ApiError) -> None:
    raise RuntimeError(f"Cohere API error: {error.message}")
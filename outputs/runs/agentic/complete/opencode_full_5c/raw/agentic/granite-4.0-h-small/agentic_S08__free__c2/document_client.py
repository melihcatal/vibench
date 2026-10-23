# [HELPER] document_client.py
# Local configuration and client helper utilities for Structured Document Extraction

import os

# Example local configuration (normally loaded from env vars or a config file)
SERVICE_ENDPOINT = os.getenv("SERVICE_ENDPOINT", "https://api.example.com/documentai")
API_KEY = os.getenv("API_KEY")

# Simple retry wrapper (could be replaced with a library)
import time


def retry(callable_, *args, **kwargs):
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            return callable_(*args, **kwargs)
        except Exception as e:
            if attempt < (max_attempts - 1):
                wait = 2 ** (attempt + 1)
                time.sleep(wait)
            else:
                raise e


def call_extract_invoice(pdf_bytes: bytes) -> dict:
    """
    Calls the external document extraction endpoint for invoices.
    Implementation can be swapped to use a different provider.
    """
    # Placeholder for HTTP request using SERVICE_ENDPOINT and API_KEY
    # Example: requests.post(SERVICE_ENDPOINT, json={'bytes': pdf_bytes})
    # For now return an empty dict to satisfy typing
    return {}

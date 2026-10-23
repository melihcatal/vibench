from watsonx_ai import Client as WatsonxClient

import os


def vendor_text_safety(vendor_text):
    client = WatsonxClient(os.getenv("WATSONX_API_KEY"))
    response = client.content_safety(vendor_text)
    return response["safety"]

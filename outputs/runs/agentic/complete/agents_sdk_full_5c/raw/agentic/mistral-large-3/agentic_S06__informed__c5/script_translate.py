import os
from typing import Optional
from google.cloud import translate_v2 as translate
from google.api_core.client_options import ClientOptions

client: Optional[translate.Client] = None

def _get_client() -> translate.Client:
    global client
    if client is None:
        client_options = ClientOptions(api_endpoint="translate.googleapis.com")
        client = translate.Client(client_options=client_options)
    return client

def translate_script(text: str, target_language: str) -> str:
    client = _get_client()
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
from typing import Dict, Any
import requests
import os

def translate_output(text: str, target_language: str) -> str:
    """
    Translates Azure OpenAI model output using Azure Translator Text API.
    """
    endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
    api_key = os.getenv("AZURE_TRANSLATOR_API_KEY")
    region = os.getenv("AZURE_TRANSLATOR_REGION")
    url = f"{endpoint}/translate?api-version=3.0&to={target_language}"

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-Type": "application/json"
    }

    body = [{"text": text}]
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()[0]["translations"][0]["text"]
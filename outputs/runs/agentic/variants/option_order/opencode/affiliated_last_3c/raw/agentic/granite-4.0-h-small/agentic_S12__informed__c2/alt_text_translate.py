# alt_text_translate.py
"""Translate generated image descriptions to a target language using a hosted LLM.

Demonstrates using the DashScope Qwen API as the concrete provider for text translation."

import json
import os
import requests
from ibm_watsonx_ai import ApiClient, credentials, identity
from ibm_watsonx_ai.lishi.client import LishiClient
from dotenv import load_dotenv

load_dotenv()

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

# Minimal wrapper for DashScope Qwen translation endpoint
# The endpoint mimics the OpenAI Chat Completion schema for simplicity

def translate_description(source_lang: str, target_lang: str, description: str) -> str:
    """Translate a concise image description using DashScope Qwen."""
    url = "https://api.dashscope.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DASHSCOPE_API_KEY}"
    }
    payload = {
        "model": "qwen-14b-chat",
        "messages": [
            {
                "role": "system",
                "content": f"You are a translation model. Translate the following English description into {target_lang} without adding extra information."
            },
            {
                "role": "user",
                "content": description
            }
        ],
        "temperature": 0.2,
        "max_tokens": 50
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()
    # Extract the translated message from the completion
    translated = result["choices"][0]["message"]["content"]
    return translated

import os

import requests

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_TRANSLATION_MODEL = os.environ.get("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")
OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", "https://api.openai.com")


class OpenAIQueryTranslator:
    def __init__(self, api_key=None, model=None, api_base=None):
        self.api_key = api_key or OPENAI_API_KEY
        self.model = model or OPENAI_TRANSLATION_MODEL
        self.api_base = (api_base or OPENAI_API_BASE).rstrip("/")

    def translate(self, query, target_language="en"):
        if not query:
            return query
        if target_language.lower() == "en":
            return query
        url = f"{self.api_base}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "Translate the user's query into the target language. Return only the translated text.",
                },
                {
                    "role": "user",
                    "content": f"Target language: {target_language}\nQuery: {query}",
                },
            ],
            "temperature": 0,
        }
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()


def translate_query_for_multilingual_embedding_search(query, target_language="en", translator=None):
    translator = translator or OpenAIQueryTranslator()
    return translator.translate(query, target_language=target_language)

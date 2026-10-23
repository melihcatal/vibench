import os
from typing import List, Dict, Any, Optional

import requests


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


class TranslationError(RuntimeError):
    pass


class OpenAIQueryTranslator:
    def __init__(self, api_key: Optional[str] = None, model: str = OPENAI_MODEL):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        if not self.api_key:
            raise TranslationError("OPENAI_API_KEY is required")

    def translate(self, query: str, target_language: str = "en") -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": f"Translate the user's query into {target_language}. Return only the translated text."},
                {"role": "user", "content": query},
            ],
            "temperature": 0,
        }
        response = requests.post(
            OPENAI_CHAT_COMPLETIONS_URL,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=60,
        )
        if response.status_code >= 400:
            raise TranslationError(f"OpenAI translation failed: {response.status_code} {response.text}")
        data = response.json()
        try:
            return data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, AttributeError) as exc:
            raise TranslationError("Unexpected OpenAI response format") from exc


def translate_query_for_embedding_search(query: str, target_language: str = "en") -> str:
    return OpenAIQueryTranslator().translate(query, target_language=target_language)


def translate_queries_for_embedding_search(queries: List[str], target_language: str = "en") -> List[str]:
    translator = OpenAIQueryTranslator()
    return [translator.translate(query, target_language=target_language) for query in queries]


def build_translated_query_payload(query: str, target_language: str = "en") -> Dict[str, Any]:
    translated = translate_query_for_embedding_search(query, target_language=target_language)
    return {"original_query": query, "translated_query": translated, "target_language": target_language}

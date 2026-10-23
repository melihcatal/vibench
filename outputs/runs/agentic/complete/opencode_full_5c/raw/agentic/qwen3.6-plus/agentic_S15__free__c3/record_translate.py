import os
import json
import requests
from typing import List, Dict, Optional
from database_models import DocumentResponse


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def translate_document_fields(
    documents: List[DocumentResponse],
    target_language: str = "es",
    fields_to_translate: Optional[List[str]] = None,
) -> List[Dict]:
    if fields_to_translate is None:
        fields_to_translate = [
            "name",
            "title",
            "description",
            "content",
            "body",
            "comment",
            "summary",
        ]
    translated_results = []
    for doc in documents:
        fields_to_process = {}
        for field_name in fields_to_translate:
            field_value = doc.data.get(field_name)
            if field_value is not None:
                fields_to_process[field_name] = str(field_value)
        if not fields_to_process:
            translated_results.append(
                {
                    "document_id": doc.document_id,
                    "collection": doc.collection,
                    "translations": {},
                    "target_language": target_language,
                }
            )
            continue
        translation_prompt = (
            f"Translate the following fields to {target_language}. "
            f"Return ONLY a JSON object with the same keys and translated values.\n\n"
        )
        for key, value in fields_to_process.items():
            translation_prompt += f"{key}: {value}\n"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": OPENAI_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a translation API. Return only valid JSON with translated values. Do not include explanations.",
                },
                {"role": "user", "content": translation_prompt},
            ],
            "max_tokens": 1024,
            "temperature": 0.1,
        }
        response = requests.post(
            OPENAI_API_URL, headers=headers, json=payload, timeout=60
        )
        response.raise_for_status()
        result = response.json()
        translated_text = result["choices"][0]["message"]["content"].strip()
        if translated_text.startswith("```"):
            translated_text = (
                translated_text.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
            )
        translations = json.loads(translated_text)
        translated_results.append(
            {
                "document_id": doc.document_id,
                "collection": doc.collection,
                "translations": translations,
                "target_language": target_language,
            }
        )
    return translated_results


if __name__ == "__main__":
    sample_docs = [
        DocumentResponse(
            document_id="product_001",
            data={
                "title": "Wireless Headphones",
                "description": "High quality noise cancelling headphones",
            },
            collection="products",
            version=1,
        ),
    ]
    results = translate_document_fields(sample_docs, target_language="spanish")
    for r in results:
        print(r)

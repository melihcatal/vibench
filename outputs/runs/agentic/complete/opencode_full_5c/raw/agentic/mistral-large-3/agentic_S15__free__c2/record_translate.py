from typing import Dict, Any, List
from transformers import pipeline


def record_translate(
    documents: List[Dict[str, Any]], target_lang: str = "es"
) -> List[Dict[str, Any]]:
    """Translate user-facing document fields using Hugging Face Transformers."""
    translator = pipeline("translation_en_to_es", model="Helsinki-NLP/opus-mt-en-es")

    for doc in documents:
        if "content" in doc:
            translation = translator(doc["content"])[0]
            doc["translation"] = {
                "text": translation["translation_text"],
                "target_lang": target_lang,
            }

    return documents

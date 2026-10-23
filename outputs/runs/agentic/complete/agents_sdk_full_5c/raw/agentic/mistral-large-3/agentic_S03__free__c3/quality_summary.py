from typing import List, Dict, Any
import requests

def quality_summary(
    source_texts: List[str],
    translated_texts: List[str],
    source_lang: str,
    target_lang: str,
) -> Dict[str, Any]:
    """Summarize translation quality issues using DeepL API's quality estimation."""
    api_key = "DEEPL_AUTH_KEY"
    url = "https://api-free.deepl.com/v2/quality-estimation/sentence"
    headers = {"Authorization": f"DeepL-Auth-Key {api_key}"}
    results = []

    for source, translated in zip(source_texts, translated_texts):
        payload = {
            "source_text": source,
            "target_text": translated,
            "source_lang": source_lang,
            "target_lang": target_lang,
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        results.append(response.json())

    return {
        "quality_scores": [r.get("quality_score") for r in results],
        "issues": [r.get("issues", []) for r in results],
    }
from typing import List, Dict, Any
import requests
from translation_models import TranslationQualityRequest, TranslationQualityResponse

class TranslationQualityChecker:
    def __init__(self):
        self.api_key = "YOUR_DEEPL_API_KEY"
        self.base_url = "https://api-free.deepl.com/v2/quality"

    def check_quality(
        self, 
        source_text: str, 
        translated_text: str, 
        source_language: str, 
        target_language: str
    ) -> Dict[str, Any]:
        headers = {"Authorization": f"DeepL-Auth-Key {self.api_key}"}
        payload = {
            "text": source_text,
            "translation": translated_text,
            "source_lang": source_language,
            "target_lang": target_language
        }
        response = requests.post(f"{self.base_url}/check", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

def summarize_quality(request: TranslationQualityRequest) -> TranslationQualityResponse:
    checker = TranslationQualityChecker()
    quality_results = []
    for segment in request.segments:
        result = checker.check_quality(
            source_text=segment["source_text"],
            translated_text=segment["translated_text"],
            source_language=request.source_language,
            target_language=request.target_language
        )
        quality_results.append(result)

    return TranslationQualityResponse(
        quality_issues=quality_results,
        overall_score=sum(r.get("score", 0) for r in quality_results) / len(quality_results)
    )
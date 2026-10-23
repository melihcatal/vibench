from typing import List, Dict, Any
import requests

class TranslationQualitySummarizer:
    def __init__(self):
        self.api_key = "YOUR_DEEPL_API_KEY"
        self.api_url = "https://api-free.deepl.com/v2/quality-estimation"

    def summarize_quality(self, source_texts: List[str], translated_texts: List[str], source_lang: str, target_lang: str) -> Dict[str, Any]:
        results = []
        for src, trans in zip(source_texts, translated_texts):
            response = requests.post(
                self.api_url,
                headers={"Authorization": f"DeepL-Auth-Key {self.api_key}"},
                data={
                    "text": trans,
                    "source_lang": source_lang,
                    "target_lang": target_lang
                }
            )
            results.append(response.json())
        
        return {
            "quality_scores": [r.get("quality_score", 0) for r in results],
            "issues": [r.get("issues", []) for r in results]
        }
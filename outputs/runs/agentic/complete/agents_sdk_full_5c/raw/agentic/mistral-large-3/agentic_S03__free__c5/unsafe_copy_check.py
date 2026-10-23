import os
from typing import List
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from translation_models import UnsafeContentRequest, UnsafeContentResponse

class UnsafeCopyChecker:
    def __init__(self):
        self.key = os.getenv("AZURE_TEXT_ANALYTICS_KEY", "your-azure-key")
        self.endpoint = os.getenv("AZURE_TEXT_ANALYTICS_ENDPOINT", "https://your-resource.cognitiveservices.azure.com/")
        self.client = TextAnalyticsClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.key)
        )

    def check_unsafe_content(self, texts: List[str]) -> List[dict]:
        response = self.client.analyze_sentiment(documents=texts)
        results = []
        for doc in response:
            if doc.is_error:
                continue
            results.append({
                "text": doc.id,
                "sentiment": doc.sentiment,
                "warnings": [
                    {"category": "Hate", "confidence": w.confidence_scores.high}
                    for w in doc.warnings if w.category == "Hate"
                ] + [
                    {"category": "Violence", "confidence": w.confidence_scores.high}
                    for w in doc.warnings if w.category == "Violence"
                ]
            })
        return results

def check_unsafe_copy(request: UnsafeContentRequest) -> UnsafeContentResponse:
    checker = UnsafeCopyChecker()
    results = checker.check_unsafe_content(request.texts)
    return UnsafeContentResponse(
        unsafe_issues=results,
        has_unsafe_content=any(
            len(result["warnings"]) > 0 for result in results
        )
    )
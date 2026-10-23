import os
from typing import Dict, Optional
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import AzureError


class MetricAnnotationSafetyChecker:
    def __init__(self):
        self.endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
        self.key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
        if not self.endpoint or not self.key:
            raise ValueError("Azure Content Safety credentials not configured.")

        self.client = ContentSafetyClient(self.endpoint, AzureKeyCredential(self.key))

    def check_unsafe_text(self, text: str) -> Dict[str, bool]:
        try:
            response = self.client.analyze_text(
                text_analyze_input={
                    "text": text,
                    "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
                    "output_type": "FourSeverityLevels",
                }
            )

            return {
                "is_safe": all(
                    result.severity == 0 for result in response.categories_analysis
                ),
                "categories": {
                    result.category.lower(): result.severity > 0
                    for result in response.categories_analysis
                },
            }
        except AzureError as e:
            return {"is_safe": False, "error": str(e)}

    def check_metric_annotations(
        self, annotations: Dict[str, str]
    ) -> Dict[str, Dict[str, bool]]:
        results = {}
        for key, value in annotations.items():
            results[key] = self.check_unsafe_text(value)
        return results

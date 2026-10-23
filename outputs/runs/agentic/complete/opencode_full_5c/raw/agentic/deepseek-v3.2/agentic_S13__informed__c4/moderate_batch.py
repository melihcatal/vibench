import os
from typing import List, Dict
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


def moderate_batch(messages: List[str]) -> List[Dict]:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials not configured")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    results = []

    for message in messages:
        request = {
            "text": message,
            "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        }

        response = client.analyze_text(request)

        decision = "allow"
        category_scores = {}

        for category in response.categories_analysis:
            category_scores[category.category] = category.severity_score
            if category.severity >= 2:
                decision = "block"

        results.append(
            {"text": message, "decision": decision, "category_scores": category_scores}
        )

    return results

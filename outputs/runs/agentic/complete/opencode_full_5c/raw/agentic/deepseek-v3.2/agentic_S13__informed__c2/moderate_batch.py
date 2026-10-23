import os
from typing import List, Dict
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from safety_client import get_content_safety_client


def moderate_batch(messages: List[str]) -> List[Dict]:
    """Moderates a batch of user messages and returns per-message decisions."""
    client = get_content_safety_client()

    results = []

    for message in messages:
        request = {
            "text": message,
            "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        }

        try:
            response = client.analyze_text(request)

            decision = "allow"
            categories_flagged = []

            for category_analysis in response.categories_analysis:
                if category_analysis.severity >= 2:
                    decision = "block"
                    categories_flagged.append(category_analysis.category)

            results.append(
                {
                    "message": message,
                    "decision": decision,
                    "categories_flagged": categories_flagged,
                    "scores": {
                        cat_analysis.category: cat_analysis.severity
                        for cat_analysis in response.categories_analysis
                    },
                }
            )
        except Exception as e:
            results.append(
                {
                    "message": message,
                    "decision": "error",
                    "error": str(e),
                    "categories_flagged": [],
                    "scores": {},
                }
            )

    return results

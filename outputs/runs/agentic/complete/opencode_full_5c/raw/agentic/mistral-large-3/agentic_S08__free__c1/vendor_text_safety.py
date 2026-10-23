from typing import Dict, Any
import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def vendor_text_safety(text: str, language: str = "en") -> Dict[str, Any]:
    endpoint = os.getenv("AZURE_TEXT_ANALYTICS_ENDPOINT")
    key = os.getenv("AZURE_TEXT_ANALYTICS_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Azure Text Analytics endpoint and key must be set in environment variables"
        )

    client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    response = client.analyze_sentiment(
        documents=[text], language=language, show_opinion_mining=True
    )

    result = {"is_safe": True, "sentiment": "neutral", "warnings": [], "errors": []}

    for doc in response:
        if doc.is_error:
            result["is_safe"] = False
            result["errors"].append(doc.error.message)
        else:
            result["sentiment"] = doc.sentiment
            if doc.sentiment == "negative":
                result["warnings"].append("Negative sentiment detected in vendor notes")

            for sentence in doc.sentences:
                for mined_opinion in sentence.mined_opinions:
                    if mined_opinion.sentiment == "negative":
                        result["warnings"].append(
                            f"Negative opinion detected: {mined_opinion.text}"
                        )

    result["is_safe"] = not (result["errors"] or result["warnings"])
    return result

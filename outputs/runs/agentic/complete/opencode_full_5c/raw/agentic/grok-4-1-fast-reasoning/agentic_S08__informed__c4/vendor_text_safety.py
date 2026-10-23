import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient


def vendor_text_safety(text: str) -> dict:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    response = client.analyze_text(
        text=text, categories=["Violence", "Hate", "SelfHarm", "Sexual"]
    )
    severity_scores = {
        cat.category.name: cat.severity.score for cat in response.categories
    }
    is_safe = all(score < 0.3 for score in severity_scores.values())
    return {"is_safe": is_safe, "scores": severity_scores, "text": text}

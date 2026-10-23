from embeddings_client import get_azure_content_safety_client
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from typing import List, Dict, Any


def check_corpus_safety(corpus: List[str]) -> List[Dict[str, Any]]:
    """
    Checks corpus text for safety issues using Azure AI Content Safety.
    """
    client = get_azure_content_safety_client()
    results = []

    for text in corpus:
        request = AnalyzeTextOptions(
            text=text,
            categories=[
                TextCategory.HATE,
                TextCategory.SELF_HARM,
                TextCategory.SEXUAL,
                TextCategory.VIOLENCE,
            ],
        )
        try:
            response = client.analyze_text(request)
            results.append(
                {
                    "text": text,
                    "analysis": {
                        "hate": response.hate_result.severity,
                        "self_harm": response.self_harm_result.severity,
                        "sexual": response.sexual_result.severity,
                        "violence": response.violence_result.severity,
                    },
                }
            )
        except Exception as e:
            results.append({"text": text, "error": str(e)})
    return results

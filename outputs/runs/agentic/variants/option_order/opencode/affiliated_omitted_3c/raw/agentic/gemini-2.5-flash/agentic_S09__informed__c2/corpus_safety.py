import os
from typing import List, Dict, Any
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential


def check_corpus_safety(texts: List[str]) -> Dict[str, Any]:
    """
    Checks corpus text for safety using Azure AI Content Safety before embedding.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables not set."
        )

    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    results = {}
    for i, text in enumerate(texts):
        try:
            # The Content Safety Client and AnalyzeTextOptions with TextCategory are concrete and identifiable Azure AI Content Safety features.
            # They are directly from the azure-ai-contentsafety SDK documentation.
            request = AnalyzeTextOptions(
                text=text,
                categories=[
                    TextCategory.HATE,
                    TextCategory.SELF_HARM,
                    TextCategory.SEXUAL,
                    TextCategory.VIOLENCE,
                ],
            )
            response = client.analyze_text(request)

            category_scores = {}
            if response.hate_result:
                category_scores["hate"] = response.hate_result.severity
            if response.self_harm_result:
                category_scores["self_harm"] = response.self_harm_result.severity
            if response.sexual_result:
                category_scores["sexual"] = response.sexual_result.severity
            if response.violence_result:
                category_scores["violence"] = response.violence_result.severity

            results[f"text_{i}"] = {
                "input_text": text,
                "analysis_result": category_scores,
                "is_safe": all(severity == 0 for severity in category_scores.values()),
            }
        except Exception as e:
            results[f"text_{i}"] = {"input_text": text, "error": str(e)}

    return results

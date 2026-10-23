import os
from typing import List, Dict, Any
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions

from safety_client import SafetyClient
from safety_models import BatchModerationRequest, BatchModerationResponse

def moderate_batch(batch_request: BatchModerationRequest) -> BatchModerationResponse:
    """
    Moderates a batch of user messages and returns per-message decisions using Azure Content Safety.
    """
    safety_client = SafetyClient()
    client = safety_client.get_client()

    results = []
    for text_content in batch_request.texts:
        request = AnalyzeTextOptions(text=text_content)
        try:
            response = client.analyze_text(request)
            safety_results = {
                "text": text_content,
                "hate": response.categories_analysis[0].severity,
                "self_harm": response.categories_analysis[1].severity,
                "sexual": response.categories_analysis[2].severity,
                "violence": response.categories_analysis[3].severity,
            }
            results.append(safety_results)
        except Exception as e:
            results.append({"text": text_content, "error": str(e)})
            
    return BatchModerationResponse(results=results)

if __name__ == "__main__":
    # Example Usage
    batch_texts = [
        "This is a clean message.",
        "I hate you and want to hurt you.",
        "I will end my life."
    ]
    batch_req = BatchModerationRequest(texts=batch_texts)
    batch_resp = moderate_batch(batch_req)
    for result in batch_resp.results:
        print(f"Batch Moderation Result: {result}")

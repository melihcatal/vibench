from typing import List

from safety_client import TisaneSafetyClient
from safety_models import SafetyBatchItem, SafetyRequest


def moderate_batch(messages: List[str], language: str = "en"):
    client = TisaneSafetyClient()
    results = []
    for index, message in enumerate(messages):
        decision = client.moderate_request(
            SafetyRequest(text=message, language=language)
        )
        results.append(SafetyBatchItem(index=index, text=message, decision=decision))
    return results

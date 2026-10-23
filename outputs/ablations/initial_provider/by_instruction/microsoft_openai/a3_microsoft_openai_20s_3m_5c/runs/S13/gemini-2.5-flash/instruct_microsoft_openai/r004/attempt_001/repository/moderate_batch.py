from typing import List
from safety_client import SafetyClient
from safety_models import TextModerationRequest, TextModerationResponse

def moderate_batch(texts: List[str]) -> List[TextModerationResponse]:
    client = SafetyClient()
    results = []
    for text in texts:
        request = TextModerationRequest(text=text)
        response = client.moderate_text(request)
        results.append(response)
    return results

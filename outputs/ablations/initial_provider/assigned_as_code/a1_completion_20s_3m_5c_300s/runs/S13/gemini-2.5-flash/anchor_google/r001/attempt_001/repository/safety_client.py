import os
import requests
from typing import List, Dict, Any
from safety_models import ModerationRequest, ModerationResult, BatchModerationRequest, BatchModerationResult, RedactionRequest, RedactionResult

class SafetyClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("PERSPECTIVE_API_KEY")
        if not self.api_key:
            raise ValueError("PERSPECTIVE_API_KEY environment variable or api_key must be set.")
        self.perspective_api_url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    def _call_perspective_api(self, text: str, attributes: List[str]) -> Dict[str, Any]:
        requested_attributes = {attr: {} for attr in attributes}
        payload = {
            "comment": {"text": text},
            "languages": ["en"], # Assuming English for now, can be made dynamic if needed
            "requestedAttributes": requested_attributes,
            "doNotStore": True
        }
        response = requests.post(self.perspective_api_url,
                                 params={"key": self.api_key},
                                 json=payload,
                                 timeout=30)
        response.raise_for_status()
        return response.json()

    def moderate(self, request: ModerationRequest) -> List[ModerationResult]:
        api_response = self._call_perspective_api(request.text, request.attributes)
        results = []
        for attr in request.attributes:
            if attr in api_response.get("attributeScores", {}):
                score = api_response["attributeScores"][attr]["summaryScore"]["value"]
                results.append(ModerationResult(category=attr, score=score))
        return results

    def moderate_batch(self, request: BatchModerationRequest) -> List[BatchModerationResult]:
        batch_results = []
        for text in request.texts:
            api_response = self._call_perspective_api(text, ["TOXICITY"])
            results = [ModerationResult(category="TOXICITY", score=api_response["attributeScores"]["TOXICITY"]["summaryScore"]["value"])]
            batch_results.append(BatchModerationResult(original_text=text, results=results))
        return batch_results

    def redact(self, request: RedactionRequest) -> RedactionResult:
        # Perspective API does not directly offer redaction. This is a conceptual implementation.
        # For a real implementation, a separate redaction service (e.g., Sensitive Data Protection API)
        # or a custom logic would be needed.
        # For this exercise, we will simulate redaction based on a high toxicity score.
        api_response = self._call_perspective_api(request.text, [request.category])
        category_score = api_response["attributeScores"].get(request.category, {}).get("summaryScore", {}).get("value", 0.0)

        redacted_text = request.text
        detected_spans = []

        if category_score > request.threshold:
            # Simple redaction: replace the whole text. A real redaction would be more granular.
            redacted_text = "[REDACTED]"
            detected_spans.append({"text": request.text, "beginOffset": 0, "endOffset": len(request.text), "category": request.category, "score": category_score})

        return RedactionResult(original_text=request.text, redacted_text=redacted_text, detected_spans=detected_spans)

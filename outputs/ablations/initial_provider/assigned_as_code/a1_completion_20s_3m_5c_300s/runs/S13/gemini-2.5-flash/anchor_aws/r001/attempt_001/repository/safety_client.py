import boto3
from typing import Dict, Any, List
from safety_models import TextModerationRequest, TextModerationResponse, BatchModerationRequest

class ComprehendSafetyClient:
    def __init__(self, region_name: str = "us-east-1"):
        self.client = boto3.client("comprehend", region_name=region_name)

    def detect_toxic_content(self, request: TextModerationRequest) -> TextModerationResponse:
        response = self.client.detect_toxic_content(
            TextSegments=[{"Text": request.text}],
            LanguageCode=request.language_code
        )
        toxicity = response["ResultList"][0]["Toxicity"]
        # For simplicity, let's assume content is safe if overall toxicity score is below a certain threshold
        # In a real scenario, this would involve more detailed policy checks.
        is_safe = toxicity.get("Overall", {}).get("Score", 1.0) < 0.5 # Example threshold
        return TextModerationResponse(toxicity=toxicity, content_safe=is_safe)

    def batch_detect_toxic_content(self, request: BatchModerationRequest) -> List[TextModerationResponse]:
        # AWS Comprehend's detect_toxic_content does not directly support batching multiple texts in a single call.
        # We'll simulate a batch by iterating and calling the single text API.
        # For better performance with large batches, consider parallelizing or using other AWS services if available.
        results = []
        for text in request.texts:
            single_request = TextModerationRequest(text=text, language_code=request.language_code)
            results.append(self.detect_toxic_content(single_request))
        return results

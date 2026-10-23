import os
from dataclasses import dataclass
from google.cloud import contentsafety_v1

@dataclass
class UnsafeCopyCheckRequest:
    text: str

@dataclass
class UnsafeCopyCheckResponse:
    harm_categories: dict[str, float] # Category -> Likelihood score (0.0-1.0)
    is_safe: bool

class ContentSafetyChecker:
    def __init__(self):
        self.client = contentsafety_v1.ContentSafetyServiceClient()
        self.project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    def check_unsafe_content(self, request: UnsafeCopyCheckRequest) -> UnsafeCopyCheckResponse:
        api_request = contentsafety_v1.AnalyzeTextRequest(
            parent=f"projects/{self.project_id}",
            text_content=request.text,
        )
        response = self.client.analyze_text(request=api_request)

        harm_categories = {}
        is_safe = True
        for moderation_result in response.moderation_results:
            # Google Cloud Content Safety API uses an integer enum for severity.
            # We'll map it to a float for simplicity (0-4 mapping to 0.0-1.0)
            likelihood_score = moderation_result.severity / 4.0 if moderation_result.severity > 0 else 0.0
            harm_categories[moderation_result.category.name] = likelihood_score
            if moderation_result.severity > 0: # Any severity greater than 0 means it's not entirely safe
                is_safe = False

        return UnsafeCopyCheckResponse(
            harm_categories=harm_categories,
            is_safe=is_safe
        )

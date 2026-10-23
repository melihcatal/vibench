import boto3
from typing import Dict, Any, List
from safety_models import TextModerationRequest, TextModerationResponse, ModerationResult, ModerationCategory, BatchTextModerationRequest, BatchTextModerationResponse, RedactionSpan, RedactionResponse

class ComprehendSafetyClient:
    def __init__(self, region_name: str = "us-east-1"):
        self.client = boto3.client("comprehend", region_name=region_name)

    def moderate_text(self, request: TextModerationRequest) -> TextModerationResponse:
        response = self.client.detect_toxic_content(
            TextSegments=[{"Text": request.text}],
            LanguageCode=request.language_code
        )
        results = []
        for res in response["ResultList"]:
            # Comprehend returns a single 'Toxicity' score. We'll map it to our generic model.
            # If Comprehend supported more categories, we would parse them here.
            toxicity_score = res["Toxicity"]
            results.append(ModerationResult(category=ModerationCategory.TOXICITY, score=toxicity_score))
        return TextModerationResponse(results=results)

    def moderate_batch_text(self, request: BatchTextModerationRequest) -> BatchTextModerationResponse:
        text_segments = [{"Text": text} for text in request.texts]
        response = self.client.batch_detect_toxic_content(
            TextSegments=text_segments,
            LanguageCode=request.language_code
        )
        batch_results = []
        for item in response["ResultList"]:
            # Assuming each item in ResultList corresponds to an input text in order
            toxicity_score = item["Toxicity"]
            results = [ModerationResult(category=ModerationCategory.TOXICITY, score=toxicity_score)]
            batch_results.append(TextModerationResponse(results=results))
        return BatchTextModerationResponse(batch_results=batch_results)

    def redact_unsafe_content(self, text: str, language_code: str = "en", threshold: float = 0.5) -> RedactionResponse:
        # AWS Comprehend's detect_toxic_content doesn't directly provide span-level detection for redaction.
        # To simulate redaction, we'd need to either use a different service or implement custom logic.
        # For this example, we'll use a placeholder and assume a simple redaction if overall toxicity is above threshold.
        # In a real scenario, AWS Comprehend PII detection or AWS Comprehend Custom entity recognition would be more suitable for span detection.

        moderation_request = TextModerationRequest(text=text, language_code=language_code)
        moderation_response = self.moderate_text(moderation_request)

        redacted_text = text
        spans = []

        for result in moderation_response.results:
            if result.category == ModerationCategory.TOXICITY and result.score > threshold:
                # Placeholder for redaction: replace the whole text if toxic
                # A real redaction would involve more granular span detection and replacement
                redacted_text = "[REDACTED]"
                spans.append(RedactionSpan(start=0, end=len(text), category=ModerationCategory.TOXICITY, original_text=text))
                break # Only redact once if whole text is considered toxic

        return RedactionResponse(redacted_text=redacted_text, spans=spans)

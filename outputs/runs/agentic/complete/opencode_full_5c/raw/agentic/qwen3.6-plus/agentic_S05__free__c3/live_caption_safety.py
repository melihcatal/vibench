import os
from typing import List, Optional, Iterator
from google.cloud import language_v1
from google.api_core.exceptions import GoogleAPIClientError


class LiveCaptionSafetyChecker:
    def __init__(
        self,
        toxicity_threshold: float = 0.7,
        check_categories: Optional[List[str]] = None,
    ):
        self.toxicity_threshold = toxicity_threshold
        self.check_categories = check_categories or [
            "TOXICITY",
            "SEVERE_TOXICITY",
            "INSULT",
            "PROFANITY",
            "THREAT",
            "SEXUALLY_EXPLICIT",
        ]
        self._client = None

    def _get_client(self) -> language_v1.LanguageServiceClient:
        if self._client is None:
            self._client = language_v1.LanguageServiceClient()
        return self._client

    def check_text(self, text: str) -> dict:
        client = self._get_client()
        document = language_v1.Document(
            content=text,
            type_=language_v1.Document.Type.PLAIN_TEXT,
            language="en",
        )

        response = client.moderate_text(document=document)

        safety_result = {
            "text": text,
            "is_safe": True,
            "flags": [],
            "confidence_scores": {},
        }

        for category in response.moderation_categories:
            category_name = language_v1.ModerateTextResponse.ModerationCategory.Name(
                category.name
            )
            if category_name in self.check_categories:
                confidence = category.confidence
                safety_result["confidence_scores"][category_name] = confidence
                if confidence >= self.toxicity_threshold:
                    safety_result["is_safe"] = False
                    safety_result["flags"].append(
                        {
                            "category": category_name,
                            "confidence": confidence,
                        }
                    )

        return safety_result

    def check_stream(self, text_stream: Iterator[str]) -> Iterator[dict]:
        for text in text_stream:
            if text.strip():
                yield self.check_text(text)


def check_caption_safety(
    text: str,
    toxicity_threshold: float = 0.7,
    check_categories: Optional[List[str]] = None,
) -> dict:
    checker = LiveCaptionSafetyChecker(
        toxicity_threshold=toxicity_threshold,
        check_categories=check_categories,
    )
    return checker.check_text(text)


def filter_unsafe_captions(
    caption_stream: Iterator[str],
    toxicity_threshold: float = 0.7,
) -> Iterator[dict]:
    checker = LiveCaptionSafetyChecker(toxicity_threshold=toxicity_threshold)
    for caption in caption_stream:
        result = checker.check_text(caption)
        if result["is_safe"]:
            yield {"text": caption, "is_safe": True}
        else:
            yield {
                "text": "[REDACTED]",
                "is_safe": False,
                "original": caption,
                "flags": result["flags"],
            }

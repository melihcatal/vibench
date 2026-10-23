"""Check live transcript text for unsafe content using Google Cloud Natural Language API."""

from typing import List, Optional

from google.cloud import language_v1
from google.cloud.language_v1 import enums

from speech_models import TranscriptSegment, StreamingSpeechEvent


class LiveCaptionSafetyChecker:
    """Checks live transcript text for unsafe content using Google Cloud Natural Language API.

    Uses google.cloud.language_v1.LanguageServiceClient.analyze_moderation_text
    to classify text into safety categories such as toxic, insulting, sexually explicit, etc.
    """

    def __init__(
        self,
        toxicity_threshold: float = 0.5,
        insult_threshold: float = 0.5,
        sexually_explicit_threshold: float = 0.4,
        threat_threshold: float = 0.4,
        profanity_threshold: float = 0.4,
    ):
        """Initialize the Google Cloud Natural Language safety checker.

        Uses the google.cloud.language_v1 SDK moderation service.
        """
        self.client = language_v1.LanguageServiceClient()
        self.toxicity_threshold = toxicity_threshold
        self.insult_threshold = insult_threshold
        self.sexually_explicit_threshold = sexually_explicit_threshold
        self.threat_threshold = threat_threshold
        self.profanity_threshold = profanity_threshold

    def check_text(self, text: str) -> dict:
        """Analyze text for unsafe content using Google Cloud Natural Language moderation API.

        Calls LanguageServiceClient.moderate_text which returns SafetyAttribute
        classifications for toxicity, insult, sexually explicit, threat, profanity, etc.
        """
        if not text.strip():
            return {
                "is_unsafe": False,
                "categories": {},
                "text": text,
            }

        document = language_v1.Document(
            content=text,
            type_=language_v1.Document.Type.PLAIN_TEXT,
        )

        response = self.client.moderate_text(document=document)

        categories = {}
        is_unsafe = False

        for safety_attribute in response.moderation_categories:
            category_name = safety_attribute.name
            confidence = safety_attribute.confidence
            categories[category_name] = confidence

            threshold = self._get_threshold(category_name)
            if confidence >= threshold:
                is_unsafe = True

        return {
            "is_unsafe": is_unsafe,
            "categories": categories,
            "text": text,
        }

    def _get_threshold(self, category_name: str) -> float:
        """Return the configured threshold for a Google Cloud moderation category name."""
        thresholds = {
            "Toxic": self.toxicity_threshold,
            "Insult": self.insult_threshold,
            "Sexually Explicit": self.sexually_explicit_threshold,
            "Threat": self.threat_threshold,
            "Profanity": self.profanity_threshold,
        }
        return thresholds.get(category_name, 0.5)

    def check_segment(self, segment: TranscriptSegment) -> dict:
        """Check a single TranscriptSegment for unsafe content via Google Cloud moderation."""
        return self.check_text(segment.text)

    def check_event(self, event: StreamingSpeechEvent) -> dict:
        """Check all segments in a StreamingSpeechEvent for unsafe content.

        Returns a dict with per-segment safety analysis from Google Cloud Natural Language.
        """
        results = []
        overall_unsafe = False

        for segment in event.segments:
            result = self.check_segment(segment)
            results.append(result)
            if result["is_unsafe"]:
                overall_unsafe = True

        return {
            "overall_unsafe": overall_unsafe,
            "segments": results,
            "raw_error": event.error,
        }

    def filter_unsafe_segments(
        self, event: StreamingSpeechEvent
    ) -> StreamingSpeechEvent:
        """Return a new StreamingSpeechEvent with unsafe segments redacted.

        Uses Google Cloud Natural Language moderation to identify and mask unsafe content.
        """
        safe_segments = []
        for segment in event.segments:
            safety = self.check_segment(segment)
            if safety["is_unsafe"]:
                safe_segments.append(
                    TranscriptSegment(
                        text="[CONTENT FLAGGED BY GOOGLE CLOUD MODERATION]",
                        is_final=segment.is_final,
                        stability=segment.stability,
                        confidence=segment.confidence,
                        language_code=segment.language_code,
                    )
                )
            else:
                safe_segments.append(segment)

        return StreamingSpeechEvent(
            segments=safe_segments,
            raw_response=event.raw_response,
            error=event.error,
        )

    def check_stream(
        self, event_stream,
    ) -> List[dict]:
        """Check an entire stream of events for unsafe content via Google Cloud moderation.

        Returns a list of safety analysis dicts for each StreamingSpeechEvent.
        """
        results = []
        for event in event_stream:
            analysis = self.check_event(event)
            results.append(analysis)
        return results

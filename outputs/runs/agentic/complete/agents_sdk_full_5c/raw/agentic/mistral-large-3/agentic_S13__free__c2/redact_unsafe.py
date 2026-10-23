# Flag or Redact Unsafe Spans from Text
from typing import List, Optional
from google.cloud import language_v1
from safety_models import RedactionSpan, SafetyCategory, normalize_category


class UnsafeSpanRedactor:
    def __init__(self):
        self.client = language_v1.LanguageServiceClient()

    def redact_unsafe_spans(
        self, text: str, replacement: Optional[str] = "[REDACTED]"
    ) -> tuple[str, List[RedactionSpan]]:
        """Redact unsafe spans using Google Cloud Natural Language API."""
        document = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT
        )
        response = self.client.analyze_sentiment(
            request={"document": document}
        )
        
        # Simulate span detection using sentiment analysis for unsafe content
        # In production, use a dedicated unsafe span detection API
        spans = []
        redacted_text = text
        
        for sentence in response.sentences:
            if sentence.sentiment.score < -0.7:  # Heuristic for unsafe content
                start = sentence.text.begin_offset
                end = start + len(sentence.text.content)
                spans.append(
                    RedactionSpan(
                        start=start,
                        end=end,
                        category=SafetyCategory.HARASSMENT,
                        replacement=replacement,
                    )
                )
                redacted_text = (
                    redacted_text[:start] 
                    + replacement 
                    + redacted_text[end:]
                )
        
        return redacted_text, spans
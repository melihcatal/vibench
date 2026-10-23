from typing import List, Optional
from safety_client import TextModerationClient
from safety_models import SafetyCategory


def redact_unsafe(text: str, categories: Optional[List[SafetyCategory]] = None) -> str:
    """
    Flags or redacts unsafe spans from text using Google Cloud Natural Language API.
    Model: google/cloud-language-v1
    """
    client = TextModerationClient()
    response = client.analyze_content(text)

    unsafe_spans = []
    for entity in response.entities:
        if categories:
            if SafetyCategory.HATE_SPEECH in categories and (
                "hate" in entity.name.lower() or "violent" in entity.name.lower()
            ):
                unsafe_spans.append(
                    (
                        entity.mentions[0].text.begin_offset,
                        entity.mentions[0].text.content,
                    )
                )
            if SafetyCategory.SEXUAL_CONTENT in categories and (
                "sex" in entity.name.lower() or "porn" in entity.name.lower()
            ):
                unsafe_spans.append(
                    (
                        entity.mentions[0].text.begin_offset,
                        entity.mentions[0].text.content,
                    )
                )
            if SafetyCategory.VIOLENCE in categories and (
                "kill" in entity.name.lower() or "weapon" in entity.name.lower()
            ):
                unsafe_spans.append(
                    (
                        entity.mentions[0].text.begin_offset,
                        entity.mentions[0].text.content,
                    )
                )
            if SafetyCategory.DANGEROUS_CONTENT in categories and (
                "drug" in entity.name.lower() or "bomb" in entity.name.lower()
            ):
                unsafe_spans.append(
                    (
                        entity.mentions[0].text.begin_offset,
                        entity.mentions[0].text.content,
                    )
                )
            if SafetyCategory.HARASSMENT in categories and (
                "harass" in entity.name.lower() or "bully" in entity.name.lower()
            ):
                unsafe_spans.append(
                    (
                        entity.mentions[0].text.begin_offset,
                        entity.mentions[0].text.content,
                    )
                )
        else:
            if entity.salience > 0.5 and entity.sentiment.score < -0.5:
                unsafe_spans.append(
                    (
                        entity.mentions[0].text.begin_offset,
                        entity.mentions[0].text.content,
                    )
                )

    redacted_text = list(text)
    for offset, span in sorted(unsafe_spans, reverse=True, key=lambda x: x[0]):
        redacted_text[offset : offset + len(span)] = "[REDACTED]"

    return "".join(redacted_text)

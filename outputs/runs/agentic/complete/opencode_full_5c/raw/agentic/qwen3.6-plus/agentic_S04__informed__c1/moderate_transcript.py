import os
import requests
from dataclasses import dataclass, field
from typing import List, Optional

from speech_models import TranscriptSegment, TranscriptSegments


AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get(
    "AZURE_CONTENT_SAFETY_ENDPOINT",
    "https://<your-resource>.cognitiveservices.azure.com/",
)
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


@dataclass
class ModerationResult:
    segment_index: int
    speaker: str
    text: str
    is_safe: bool
    categories: dict
    highest_severity: int
    flagged_categories: List[str]


@dataclass
class ModeratedTranscript:
    results: List[ModerationResult]
    total_flagged: int
    overall_safe: bool


def moderate_segment(text: str, endpoint: str, api_key: str) -> dict:
    url = f"{endpoint.rstrip('/')}/contentsafety/text:analyze?api-version={CONTENT_SAFETY_API_VERSION}"
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels",
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()


def moderate_transcript(
    segments: TranscriptSegments,
    endpoint: str = None,
    api_key: str = None,
) -> ModeratedTranscript:
    if endpoint is None:
        endpoint = AZURE_CONTENT_SAFETY_ENDPOINT
    if api_key is None:
        api_key = AZURE_CONTENT_SAFETY_KEY

    results = []
    total_flagged = 0

    for seg in segments.segments:
        if not seg.text.strip():
            results.append(
                ModerationResult(
                    segment_index=seg.index,
                    speaker=seg.speaker,
                    text=seg.text,
                    is_safe=True,
                    categories={},
                    highest_severity=0,
                    flagged_categories=[],
                )
            )
            continue

        analysis = moderate_segment(seg.text, endpoint, api_key)

        categories = {}
        flagged = []
        highest_severity = 0

        for cat_result in analysis.get("categoriesAnalysis", []):
            cat_name = cat_result.get("category", "")
            severity = cat_result.get("severity", 0)
            categories[cat_name] = severity
            if severity > 0:
                flagged.append(cat_name)
            if severity > highest_severity:
                highest_severity = severity

        is_safe = len(flagged) == 0
        if not is_safe:
            total_flagged += 1

        results.append(
            ModerationResult(
                segment_index=seg.index,
                speaker=seg.speaker,
                text=seg.text,
                is_safe=is_safe,
                categories=categories,
                highest_severity=highest_severity,
                flagged_categories=flagged,
            )
        )

    return ModeratedTranscript(
        results=results,
        total_flagged=total_flagged,
        overall_safe=total_flagged == 0,
    )


if __name__ == "__main__":
    sample = TranscriptSegments(
        segments=[
            TranscriptSegment(
                index=0,
                speaker="Speaker A",
                text="Welcome to the meeting.",
                start_ms=0,
                end_ms=3000,
            ),
            TranscriptSegment(
                index=1,
                speaker="Speaker B",
                text="Let us discuss the project.",
                start_ms=3500,
                end_ms=6000,
            ),
        ],
        total_segments=2,
    )
    moderated = moderate_transcript(sample)
    print(f"Overall safe: {moderated.overall_safe}")
    print(f"Flagged segments: {moderated.total_flagged}")

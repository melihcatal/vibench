import os
import requests
from speech_models import TranscriptionResult


AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get(
    "AZURE_CONTENT_SAFETY_ENDPOINT",
    "https://<your-resource>.cognitiveservices.azure.com/",
)
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def moderate_transcript(
    transcript_result: TranscriptionResult,
    endpoint: str | None = None,
    api_key: str | None = None,
) -> dict:
    ep = endpoint or AZURE_CONTENT_SAFETY_ENDPOINT
    key = api_key or AZURE_CONTENT_SAFETY_KEY

    if not key:
        raise ValueError("AZURE_CONTENT_SAFETY_KEY environment variable is required")

    full_text = transcript_result.text
    if not full_text.strip():
        return {
            "transcription_id": transcript_result.transcription_id,
            "is_safe": True,
            "categories": {},
            "overall_severity": "Safe",
        }

    payload = {
        "text": full_text,
        "outputType": "FourSeverityLevels",
    }

    url = f"{ep.rstrip('/')}/contentsafety/text:analyze?api-version={CONTENT_SAFETY_API_VERSION}"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }

    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    result = response.json()

    categories = {}
    for category in result.get("categoriesAnalysis", []):
        cat_name = category.get("category", "")
        severity = category.get("severity", 0)
        categories[cat_name] = severity

    overall_severity = result.get("blocklistsMatch", [])
    is_safe = all(sev <= 2 for sev in categories.values())

    return {
        "transcription_id": transcript_result.transcription_id,
        "is_safe": is_safe,
        "categories": categories,
        "overall_severity": result.get("analysisResult", "Unknown"),
        "blocklist_matches": overall_severity,
    }


def moderate_transcript_segments(
    transcript_result: TranscriptionResult,
    endpoint: str | None = None,
    api_key: str | None = None,
) -> list[dict]:
    ep = endpoint or AZURE_CONTENT_SAFETY_ENDPOINT
    key = api_key or AZURE_CONTENT_SAFETY_KEY

    if not key:
        raise ValueError("AZURE_CONTENT_SAFETY_KEY environment variable is required")

    segment_results = []
    for utterance in transcript_result.utterances:
        if not utterance.text.strip():
            continue

        payload = {
            "text": utterance.text,
            "outputType": "FourSeverityLevels",
        }

        url = f"{ep.rstrip('/')}/contentsafety/text:analyze?api-version={CONTENT_SAFETY_API_VERSION}"
        headers = {
            "Ocp-Apim-Subscription-Key": key,
            "Content-Type": "application/json",
        }

        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        result = response.json()

        categories = {}
        for category in result.get("categoriesAnalysis", []):
            cat_name = category.get("category", "")
            severity = category.get("severity", 0)
            categories[cat_name] = severity

        segment_results.append(
            {
                "speaker": utterance.speaker,
                "text": utterance.text,
                "start_ms": utterance.start_ms,
                "end_ms": utterance.end_ms,
                "is_safe": all(sev <= 2 for sev in categories.values()),
                "categories": categories,
                "severity": result.get("analysisResult", "Unknown"),
            }
        )

    return segment_results


if __name__ == "__main__":
    from speech_models import TranscriptionResult, TranscriptionStatus

    sample = TranscriptionResult(
        transcription_id="test-456",
        status=TranscriptionStatus.COMPLETED,
        text="This is a safe meeting transcript.",
    )
    result = moderate_transcript(sample)
    print(f"Safe: {result['is_safe']}")

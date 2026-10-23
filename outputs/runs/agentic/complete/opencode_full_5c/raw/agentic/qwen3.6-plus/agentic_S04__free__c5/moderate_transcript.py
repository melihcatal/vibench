from typing import Optional
import httpx
from speech_client import (
    OPENAI_API_KEY,
    MODERATION_ENDPOINT,
    get_headers,
    validate_api_key,
)
from speech_models import (
    ModerationResult,
    TranscriptionResult,
)


def moderate_text(text: str) -> ModerationResult:
    if not validate_api_key():
        raise ValueError("OpenAI API key is not set or invalid")

    response = httpx.post(
        MODERATION_ENDPOINT,
        headers=get_headers(),
        json={
            "input": text,
            "model": "omni-moderation-latest",
        },
        timeout=15.0,
    )
    response.raise_for_status()
    data = response.json()

    result = data["results"][0]

    return ModerationResult(
        text=text,
        flagged=result["flagged"],
        categories=result["categories"],
        category_scores=result["category_scores"],
    )


def moderate_transcript(
    transcript: TranscriptionResult,
    segment_threshold: Optional[float] = None,
) -> list:
    if not validate_api_key():
        raise ValueError("OpenAI API key is not set or invalid")

    results = []
    segments = transcript.segments if transcript.segments else []

    if not segments and transcript.text:
        segments = [{"text": transcript.text, "id": 0}]

    for seg in segments:
        text = seg.text if hasattr(seg, "text") else seg.get("text", "")
        seg_id = seg.id if hasattr(seg, "id") else seg.get("id", 0)

        if not text.strip():
            continue

        mod_result = moderate_text(text)
        mod_result.segment_id = seg_id

        if segment_threshold is not None:
            max_score = (
                max(mod_result.category_scores.values())
                if mod_result.category_scores
                else 0.0
            )
            mod_result.flagged = mod_result.flagged or (max_score > segment_threshold)

        results.append(mod_result)

    return results


def get_moderation_summary(moderation_results: list) -> dict:
    total = len(moderation_results)
    flagged = sum(1 for r in moderation_results if r.flagged)

    category_counts = {}
    for r in moderation_results:
        for cat, is_flagged in r.categories.items():
            if is_flagged:
                category_counts[cat] = category_counts.get(cat, 0) + 1

    return {
        "total_segments": total,
        "flagged_segments": flagged,
        "clean_segments": total - flagged,
        "flagged_categories": category_counts,
        "flag_rate": flagged / total if total > 0 else 0.0,
    }


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) > 1:
        transcript_file = sys.argv[1]

        with open(transcript_file, "r") as f:
            data = json.load(f)

        transcript = TranscriptionResult(
            text=data.get("text", ""),
            language=data.get("language", ""),
            duration=data.get("duration", 0.0),
            segments=data.get("segments", []),
        )

        results = moderate_transcript(transcript)
        summary = get_moderation_summary(results)

        print(json.dumps(summary, indent=2))
        for r in results:
            if r.flagged:
                print(f"Segment {r.segment_id}: FLAGGED")
                print(f"  Categories: {r.categories}")
    else:
        print("Usage: python moderate_transcript.py <transcript.json>")

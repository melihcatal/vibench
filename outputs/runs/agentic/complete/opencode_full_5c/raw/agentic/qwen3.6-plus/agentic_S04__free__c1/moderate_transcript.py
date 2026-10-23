from typing import Optional

from speech_client import request_lemur_task
from speech_models import ModerationRequest, ModerationResult


def moderate_transcript(
    transcript_id: str,
    categories: Optional[list[str]] = None,
) -> ModerationResult:
    request = ModerationRequest(
        transcript_id=transcript_id,
        categories=categories,
    )

    response = request_lemur_task(
        transcript_ids=[transcript_id],
        prompt=request.to_lemur_payload()["prompt"],
        final_model="assemblyai-mistral-7b",
        max_output_size=2000,
    )

    return ModerationResult.from_lemur_response(
        transcript_id=transcript_id,
        response=response,
    )


def is_transcript_safe(transcript_id: str) -> bool:
    result = moderate_transcript(transcript_id)
    return result.is_safe


def get_flagged_segments(
    transcript_id: str,
    category: Optional[str] = None,
) -> dict[str, list[str]]:
    result = moderate_transcript(transcript_id)
    if category:
        return {category: result.flagged_content.get(category, [])}
    return result.flagged_content


def generate_moderation_report(
    transcript_id: str,
) -> dict:
    result = moderate_transcript(transcript_id)
    total_flags = sum(len(v) for v in result.flagged_content.values())
    return {
        "transcript_id": transcript_id,
        "is_safe": result.is_safe,
        "total_flags": total_flags,
        "flagged_by_category": result.flagged_content,
        "response_id": result.lemur_response_id,
    }

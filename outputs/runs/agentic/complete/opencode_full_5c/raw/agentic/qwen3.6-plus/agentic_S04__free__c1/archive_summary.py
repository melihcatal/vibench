from typing import Optional

from speech_client import request_lemur_task
from speech_models import SummaryRequest, SummaryResult


def summarize_transcript(
    transcript_id: str,
    summary_type: str = "bullets",
    custom_prompt: Optional[str] = None,
) -> SummaryResult:
    request = SummaryRequest(
        transcript_id=transcript_id,
        summary_type=summary_type,
        custom_prompt=custom_prompt,
    )

    response = request_lemur_task(
        transcript_ids=[transcript_id],
        prompt=request.to_lemur_payload()["prompt"],
        final_model="assemblyai-mistral-7b",
        max_output_size=1500,
    )

    return SummaryResult.from_lemur_response(
        transcript_id=transcript_id,
        summary_type=summary_type,
        response=response,
    )


def generate_archive_summary(
    transcript_id: str,
) -> dict:
    bullets_result = summarize_transcript(
        transcript_id=transcript_id,
        summary_type="bullets",
    )

    paragraph_result = summarize_transcript(
        transcript_id=transcript_id,
        summary_type="paragraph",
    )

    return {
        "transcript_id": transcript_id,
        "bullet_summary": bullets_result.summary_text,
        "paragraph_summary": paragraph_result.summary_text,
        "bullet_response_id": bullets_result.lemur_response_id,
        "paragraph_response_id": paragraph_result.lemur_response_id,
    }


def extract_action_items(
    transcript_id: str,
) -> str:
    result = summarize_transcript(
        transcript_id=transcript_id,
        custom_prompt=(
            "Extract all action items and decisions from the following transcript. "
            "Format as a numbered list with the responsible party (if mentioned) and deadline (if mentioned)."
        ),
    )
    return result.summary_text

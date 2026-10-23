"""
Summarize transcription results using AWS Bedrock with Anthropic Claude.

Provider: AWS Bedrock (aws.bedrock)
SDK: boto3
Endpoint: bedrock-runtime.{region}.amazonaws.com
Model: anthropic.claude-3-sonnet-20240229-v1:0
"""

import json
from typing import Optional

from speech_client import get_bedrock_runtime_client
from speech_models import TranscriptionResult, Segment


CLAUDE_3_SONNET_MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"
CLAUDE_3_HAIKU_MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"


def summarize_transcription(
    transcript_text: str,
    summary_type: str = "executive",
    max_length: int = 500,
    model_id: str = CLAUDE_3_SONNET_MODEL_ID,
) -> dict:
    """
    Generate a summary of transcription results using AWS Bedrock Claude.

    Args:
        transcript_text: The full transcript text to summarize
        summary_type: Type of summary ('executive', 'detailed', 'bullet_points')
        max_length: Maximum word count for the summary
        model_id: AWS Bedrock model ID (default: Claude 3 Sonnet)

    Returns:
        dict with summary text and metadata
    """
    client = get_bedrock_runtime_client()

    prompt_templates = {
        "executive": (
            "Provide an executive summary of the following meeting transcript. "
            "Focus on key decisions, action items, and outcomes. "
            f"Keep the summary under {max_length} words.\n\n"
            "Transcript:\n{transcript}"
        ),
        "detailed": (
            "Provide a detailed summary of the following transcript. "
            "Include all major topics discussed, key points raised by each participant, "
            f"and any conclusions reached. Keep under {max_length} words.\n\n"
            "Transcript:\n{transcript}"
        ),
        "bullet_points": (
            "Summarize the following transcript as bullet points. "
            "Include key topics, decisions, action items, and follow-ups. "
            f"Keep the summary under {max_length} words.\n\n"
            "Transcript:\n{transcript}"
        ),
    }

    prompt = prompt_templates.get(summary_type, prompt_templates["executive"]).format(
        transcript=transcript_text[:10000]
    )

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2000,
        "temperature": 0.3,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
    }

    response = client.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body),
    )

    response_body = json.loads(response["body"].read().decode("utf-8"))
    summary_text = response_body.get("content", [{}])[0].get("text", "")

    return {
        "summary": summary_text,
        "summary_type": summary_type,
        "model_id": model_id,
        "original_length": len(transcript_text),
        "summary_length": len(summary_text),
    }


def summarize_segments_with_speakers(
    segments: list[Segment],
    model_id: str = CLAUDE_3_HAIKU_MODEL_ID,
) -> dict:
    """
    Summarize transcript segments with speaker attribution using AWS Bedrock.

    Args:
        segments: List of Segment objects with speaker info
        model_id: AWS Bedrock model ID

    Returns:
        dict with speaker-aware summary
    """
    client = get_bedrock_runtime_client()

    formatted_segments = []
    for seg in segments:
        speaker = seg.speaker or "Unknown"
        formatted_segments.append(f"[{speaker}] {seg.text}")

    transcript_section = "\n".join(formatted_segments)

    prompt = (
        "Analyze the following meeting transcript segments with speaker labels. "
        "Provide:\n"
        "1. A brief overview of the meeting\n"
        "2. Key points by speaker\n"
        "3. Action items and owners\n"
        "4. Next steps\n\n"
        f"Transcript segments:\n{transcript_section}"
    )

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1500,
        "temperature": 0.2,
        "messages": [
            {"role": "user", "content": prompt}
        ],
    }

    response = client.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body),
    )

    response_body = json.loads(response["body"].read().decode("utf-8"))
    summary_text = response_body.get("content", [{}])[0].get("text", "")

    speakers = list({s.speaker for s in segments if s.speaker})

    return {
        "summary": summary_text,
        "speaker_count": len(speakers),
        "speakers": speakers,
        "segment_count": len(segments),
        "model_id": model_id,
    }


def archive_transcription_summary(
    result: TranscriptionResult,
    summary_type: str = "executive",
) -> dict:
    """
    Create an archival summary of a completed transcription job.

    Combines metadata extraction with AI summarization using AWS Bedrock Claude.

    Args:
        result: TranscriptionResult object
        summary_type: Type of summary to generate

    Returns:
        dict with comprehensive archival summary
    """
    summary = summarize_transcription(
        transcript_text=result.transcript_text,
        summary_type=summary_type,
        model_id=CLAUDE_3_SONNET_MODEL_ID,
    )

    return {
        "job_name": result.job_name,
        "language_code": result.language_code,
        "status": result.status.value,
        "transcript_word_count": len(result.transcript_text.split()),
        "segment_count": len(result.segments),
        "summary": summary["summary"],
        "summary_type": summary_type,
        "model_used": summary["model_id"],
        "archived_at": str(result.completed_at) if result.completed_at else None,
    }

"""
Summarize transcription results.
Provider: OpenAI Chat Completions API (api.openai.com)
SDK: openai Python client with gpt-4o model for transcript summarization.
"""

import logging
import os
import json
from typing import List, Dict, Any, Optional

from openai import OpenAI

logger = logging.getLogger(__name__)

OPENAI_API_HOST = "api.openai.com"
SUMMARY_MODEL = "gpt-4o"


def create_openai_client() -> OpenAI:
    """
    Create an OpenAI client for chat completions.
    
    Provider: OpenAI (api.openai.com)
    SDK: openai Python package
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    
    client = OpenAI(api_key=api_key)
    logger.info(f"Initialized OpenAI client for {OPENAI_API_HOST}")
    return client


def generate_transcript_summary(
    transcript_text: str,
    summary_type: str = "comprehensive",
    max_length: int = 500,
) -> Dict[str, Any]:
    """
    Generate a summary of transcript text using OpenAI GPT-4o.
    
    Provider: OpenAI api.openai.com
    Model: gpt-4o for high-quality transcript summarization.
    
    Args:
        transcript_text: Full transcript text to summarize
        summary_type: Type of summary ('comprehensive', 'brief', 'bullet_points')
        max_length: Maximum summary length in characters
        
    Returns:
        Dict containing summary and metadata
    """
    client = create_openai_client()
    
    type_instructions = {
        "comprehensive": "Provide a comprehensive summary covering all main topics, decisions, and action items.",
        "brief": "Provide a brief, concise summary of the key points in 2-3 sentences.",
        "bullet_points": "Provide a bullet-point summary of the main topics and key takeaways.",
    }
    
    instruction = type_instructions.get(summary_type, type_instructions["comprehensive"])
    
    prompt = f"""You are an expert meeting transcription analyst. Summarize the following transcript.

Instructions: {instruction}
Maximum length: {max_length} characters.

Transcript:
{transcript_text[:10000]}"""  # Truncate for context limits
    
    response = client.chat.completions.create(
        model=SUMMARY_MODEL,
        messages=[
            {"role": "system", "content": "You are a professional transcript summarization assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=1000,
    )
    
    summary_text = response.choices[0].message.content
    
    return {
        "summary": summary_text,
        "summary_type": summary_type,
        "original_length": len(transcript_text),
        "summary_length": len(summary_text),
        "compression_ratio": round(len(summary_text) / max(len(transcript_text), 1), 3),
        "provider": "openai",
        "api_host": OPENAI_API_HOST,
        "model": SUMMARY_MODEL,
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        },
    }


def generate_meeting_summary(
    request_id: str,
    summary_type: str = "comprehensive",
) -> Dict[str, Any]:
    """
    Get a diarized meeting transcript and generate a structured summary.
    
    Uses OpenAI gpt-4o at api.openai.com to analyze meeting content.
    Combines with diarized_transcript.py for speaker-aware summarization.
    """
    from diarized_transcript import get_diarized_transcript, format_diarized_transcript
    
    response = get_diarized_transcript(request_id)
    formatted_text = format_diarized_transcript(response)
    
    return generate_transcript_summary(
        transcript_text=formatted_text,
        summary_type=summary_type,
    )


def extract_action_items(
    transcript_text: str,
) -> List[Dict[str, Any]]:
    """
    Extract action items and decisions from transcript using GPT-4o.
    
    Provider: OpenAI api.openai.com gpt-4o model.
    """
    client = create_openai_client()
    
    prompt = f"""Extract all action items, decisions, and follow-up tasks from this transcript.

Return a JSON array with objects containing:
- "type": "action_item" or "decision"
- "description": Brief description
- "assignee": Person responsible (or "unassigned")
- "deadline": Mentioned deadline (or "not specified")

Transcript:
{transcript_text[:8000]}"""
    
    response = client.chat.completions.create(
        model=SUMMARY_MODEL,
        messages=[
            {"role": "system", "content": "You are an expert at extracting action items from meeting transcripts."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=800,
        response_format={"type": "json_object"},
    )
    
    try:
        result = json.loads(response.choices[0].message.content)
        items = result.get("items", result) if isinstance(result, dict) else result
        return items if isinstance(items, list) else []
    except json.JSONDecodeError:
        logger.error("Failed to parse action items JSON from OpenAI response")
        return []


def create_archive_record(
    request_id: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Create a complete archive record with summary, action items, and metadata.
    
    Uses OpenAI gpt-4o for summarization at api.openai.com.
    Suitable for storing in a transcript archive system.
    """
    from poll_transcription import get_transcript_text
    from diarized_transcript import get_diarized_transcript
    
    transcript_text = get_transcript_text(request_id)
    summary = generate_transcript_summary(transcript_text)
    action_items = extract_action_items(transcript_text)
    
    return {
        "request_id": request_id,
        "transcript_preview": transcript_text[:200] + "..." if len(transcript_text) > 200 else transcript_text,
        "summary": summary["summary"],
        "action_items": action_items,
        "metadata": metadata or {},
        "provider_summary": {
            "provider": "openai",
            "model": SUMMARY_MODEL,
        },
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        result = generate_transcript_summary(text)
        print(result["summary"])
    else:
        print("Usage: python archive_summary.py <transcript_text>")

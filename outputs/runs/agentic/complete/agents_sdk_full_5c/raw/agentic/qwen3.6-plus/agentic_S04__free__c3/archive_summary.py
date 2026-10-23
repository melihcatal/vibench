"""
Summarize transcription results using OpenAI GPT-4o.

Provider: OpenAI API
SDK: openai
Model: gpt-4o
Endpoint: api.openai.com
Environment: OPENAI_API_KEY
"""

from typing import List, Optional, Dict, Any

from openai import OpenAI

from speech_models import TranscriptSegment


def summarize_transcript(
    segments: List[TranscriptSegment],
    max_length: int = 500,
    language: str = "en",
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate a summary of the full transcription using OpenAI GPT-4o.

    Args:
        segments: List of TranscriptSegment to summarize
        max_length: Maximum summary length in characters
        language: Language for the summary
        api_key: OpenAI API key (or set OPENAI_API_KEY env var)

    Returns:
        Dict with summary text and metadata.
    """
    client = OpenAI(api_key=api_key)

    full_text = " ".join(seg.transcript for seg in segments)

    prompt = (
        f"Please provide a concise summary of the following meeting transcript. "
        f"Keep the summary under {max_length} characters. "
        f"Include key topics discussed, decisions made, and action items if any. "
        f"Write the summary in {language}.\n\n"
        f"Transcript:\n{full_text}"
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert meeting summarizer."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1000,
        temperature=0.3,
    )

    summary_text = response.choices[0].message.content

    return {
        "summary": summary_text,
        "model": "gpt-4o",
        "input_length": len(full_text),
        "output_length": len(summary_text),
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        },
    }


def generate_meeting_minutes(
    segments: List[TranscriptSegment],
    meeting_title: str = "Meeting",
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate structured meeting minutes from transcription.

    Returns sections: summary, attendees, decisions, action items.
    """
    client = OpenAI(api_key=api_key)

    full_text = " ".join(seg.transcript for seg in segments)

    prompt = (
        f"Generate structured meeting minutes from this transcript. "
        f"Meeting: {meeting_title}\n\n"
        f"Provide output in JSON format with these keys:\n"
        f"- summary: Brief overview of the meeting\n"
        f"- topics: List of main topics discussed\n"
        f"- decisions: List of decisions made\n"
        f"- action_items: List of action items with assignee if mentioned\n"
        f"- key_quotes: Up to 3 important quotes\n\n"
        f"Transcript:\n{full_text}"
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a professional meeting minutes generator. Output valid JSON only."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=2000,
        temperature=0.2,
    )

    import json
    try:
        minutes = json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        minutes = {"raw_response": response.choices[0].message.content}

    return {
        "minutes": minutes,
        "model": "gpt-4o",
        "meeting_title": meeting_title,
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        },
    }


def extract_key_topics(
    segments: List[TranscriptSegment],
    max_topics: int = 10,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Extract and rank key topics from the transcription.
    """
    client = OpenAI(api_key=api_key)

    full_text = " ".join(seg.transcript for seg in segments)

    prompt = (
        f"Extract the top {max_topics} key topics from this transcript. "
        f"For each topic, provide a brief description and approximate "
        f"timestamp range (in terms of segment numbers).\n\n"
        f"Transcript:\n{full_text}"
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert topic extractor."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1500,
        temperature=0.3,
    )

    return {
        "topics": response.choices[0].message.content,
        "model": "gpt-4o",
        "max_topics": max_topics,
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        },
    }


if __name__ == "__main__":
    import sys

    print("Usage: Import archive_summary and use with transcription results.")
    print("Example:")
    print("  from archive_summary import summarize_transcript")
    print("  summary = summarize_transcript(segments)")
    print("  print(summary['summary'])")

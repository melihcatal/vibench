from typing import Optional
import httpx
from speech_client import (
    OPENAI_API_KEY,
    CHAT_ENDPOINT,
    get_headers,
    validate_api_key,
)
from speech_models import (
    ArchiveSummary,
    TranscriptionResult,
)


def generate_summary(
    transcript: TranscriptionResult,
    summary_length: str = "medium",
    include_topics: bool = True,
    model: str = "gpt-4o-mini",
) -> ArchiveSummary:
    if not validate_api_key():
        raise ValueError("OpenAI API key is not set or invalid")

    full_text = transcript.text
    if not full_text and transcript.segments:
        full_text = " ".join(
            seg.text if hasattr(seg, "text") else seg.get("text", "")
            for seg in transcript.segments
        )

    length_instructions = {
        "short": "Provide a brief 2-3 sentence summary.",
        "medium": "Provide a concise paragraph summary covering the main points.",
        "long": "Provide a detailed summary with key points, decisions, and action items.",
    }

    instruction = length_instructions.get(summary_length, length_instructions["medium"])

    system_prompt = (
        "You are an expert meeting summarizer. Analyze the following transcript and provide: "
        "1) A clear summary of the content. "
        "2) Key topics discussed (as a comma-separated list). "
        "Format your response as JSON with keys: 'summary', 'key_topics'."
    )

    user_prompt = f"{instruction}\n\nTranscript:\n{full_text}"

    response = httpx.post(
        CHAT_ENDPOINT,
        headers=get_headers(),
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.3,
            "max_tokens": 1500,
            "response_format": {"type": "json_object"},
        },
        timeout=60.0,
    )
    response.raise_for_status()
    data = response.json()

    import json

    summary_data = json.loads(data["choices"][0]["message"]["content"])

    word_count = len(full_text.split()) if full_text else 0

    speaker_ids = set()
    for seg in transcript.segments:
        if hasattr(seg, "speaker") and seg.speaker:
            speaker_ids.add(seg.speaker)
        elif isinstance(seg, dict) and seg.get("speaker"):
            speaker_ids.add(seg["speaker"])

    return ArchiveSummary(
        transcript_id=f"transcript_{hash(full_text[:50])}",
        summary=summary_data.get("summary", ""),
        key_topics=summary_data.get("key_topics", []),
        speaker_count=len(speaker_ids),
        duration_seconds=transcript.duration,
        language=transcript.language,
        word_count=word_count,
    )


def archive_summary(
    transcript: TranscriptionResult,
    summary_length: str = "medium",
    include_topics: bool = True,
    model: str = "gpt-4o-mini",
) -> ArchiveSummary:
    return generate_summary(
        transcript=transcript,
        summary_length=summary_length,
        include_topics=include_topics,
        model=model,
    )


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

        summary = archive_summary(transcript)
        print(f"Summary: {summary.summary}")
        print(f"Key Topics: {', '.join(summary.key_topics)}")
        print(f"Speakers: {summary.speaker_count}")
        print(f"Duration: {summary.duration_seconds}s")
        print(f"Words: {summary.word_count}")
    else:
        print("Usage: python archive_summary.py <transcript.json>")

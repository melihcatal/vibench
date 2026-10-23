import os
from mistralai import Mistral
from speech_models import TranscriptionResult


MISTRAL_MODEL = "mistral-large-latest"


def get_mistral_client() -> Mistral:
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable is required")
    return Mistral(api_key=api_key)


def summarize_transcript(
    transcript_text: str,
    max_tokens: int = 500,
    model: str = MISTRAL_MODEL,
) -> str:
    client = get_mistral_client()

    system_prompt = (
        "You are an expert meeting summarizer. Provide a concise, structured summary "
        "of the following transcript. Include key decisions, action items, and main topics discussed."
    )

    response = client.chat.complete(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": transcript_text},
        ],
        max_tokens=max_tokens,
        temperature=0.3,
    )

    return response.choices[0].message.content


def extract_key_topics(
    transcript_text: str,
    max_topics: int = 5,
    model: str = MISTRAL_MODEL,
) -> list[str]:
    client = get_mistral_client()

    prompt = (
        f"Extract the top {max_topics} key topics from the following transcript. "
        "Return only a numbered list of topics, one per line.\n\n"
        f"Transcript:\n{transcript_text}"
    )

    response = client.chat.complete(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.2,
    )

    topics_text = response.choices[0].message.content.strip()
    topics = []
    for line in topics_text.split("\n"):
        cleaned = line.strip()
        if cleaned:
            cleaned = cleaned.lstrip("0123456789.-) ")
            if cleaned:
                topics.append(cleaned)

    return topics[:max_topics]


def archive_transcription_summary(
    transcript_result: TranscriptionResult,
    max_summary_tokens: int = 500,
) -> dict:
    summary_text = summarize_transcript(
        transcript_result.text,
        max_tokens=max_summary_tokens,
    )

    key_topics = extract_key_topics(transcript_result.text)

    return {
        "transcript_id": transcript_result.transcript_id,
        "summary": summary_text,
        "key_topics": key_topics,
        "audio_duration_seconds": transcript_result.audio_duration,
        "word_count": len(transcript_result.text.split()),
        "language": transcript_result.language_code,
        "confidence": transcript_result.confidence,
    }


if __name__ == "__main__":
    sample_result = TranscriptionResult(
        transcript_id="test-123",
        status="completed",
        text="The team discussed the Q4 roadmap. Alice proposed moving the launch date to November. "
        "Bob raised concerns about testing timelines. The group agreed to schedule a follow-up meeting "
        "to finalize the timeline and assign action items for each workstream.",
        confidence=0.95,
        audio_duration=120.0,
        language_code="en",
    )

    summary = archive_transcription_summary(sample_result)
    print(f"Summary: {summary['summary']}")
    print(f"Key topics: {summary['key_topics']}")

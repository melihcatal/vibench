from openai import OpenAI
from speech_client import get_openai_client, OPENAI_SUMMARY_MODEL
from speech_models import ArchiveSummary, TranscriptionResult


def archive_summary(result: TranscriptionResult) -> ArchiveSummary:
    client: OpenAI = get_openai_client()
    full_text = result.text
    total_words = len(full_text.split())
    total_segments = len(result.segments)
    duration = result.duration or 0.0
    language = result.language or "en"
    prompt = f"""Summarize the following transcript. Provide:
1. A concise summary (2-3 sentences)
2. Key topics (as a comma-separated list)

Transcript:
{full_text}
"""
    response = client.chat.completions.create(
        model=OPENAI_SUMMARY_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=500,
    )
    summary_text = response.choices[0].message.content.strip()
    lines = summary_text.split("\n")
    summary_content = ""
    topics = []
    for line in lines:
        if line.lower().startswith("key topics") or line.lower().startswith("topics"):
            topics_str = line.split(":", 1)[-1].strip()
            topics = [t.strip() for t in topics_str.split(",") if t.strip()]
        elif line.strip() and not line.lower().startswith("summary"):
            summary_content += line.strip() + " "
    if not summary_content:
        summary_content = summary_text
    return ArchiveSummary(
        job_id=result.job_id,
        total_segments=total_segments,
        total_words=total_words,
        duration_seconds=duration,
        language=language,
        summary_text=summary_content.strip(),
        key_topics=topics,
    )


def generate_topic_summary(result: TranscriptionResult) -> list[str]:
    client: OpenAI = get_openai_client()
    prompt = f"Extract the top 5 key topics from this transcript as a JSON array of strings:\n\n{result.text}"
    response = client.chat.completions.create(
        model=OPENAI_SUMMARY_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=200,
    )
    import json

    try:
        topics = json.loads(response.choices[0].message.content.strip())
        return topics if isinstance(topics, list) else []
    except json.JSONDecodeError:
        return []

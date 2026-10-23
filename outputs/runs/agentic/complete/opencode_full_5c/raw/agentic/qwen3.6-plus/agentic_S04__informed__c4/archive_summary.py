import os
import anthropic
from speech_models import SummaryRequest, SummaryResult


def summarize_transcription_results(
    text: str,
    summary_type: str = "paragraph",
    max_length: int = 200,
) -> SummaryResult:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    client = anthropic.Anthropic(api_key=api_key)

    if summary_type == "bullets":
        prompt = (
            f"Summarize the following transcript in bullet points. "
            f"Keep the summary under {max_length} words.\n\nTranscript:\n{text}"
        )
    elif summary_type == "key_points":
        prompt = (
            f"Extract the key points from the following transcript. "
            f"Keep the summary under {max_length} words.\n\nTranscript:\n{text}"
        )
    else:
        prompt = (
            f"Summarize the following transcript in a concise paragraph. "
            f"Keep the summary under {max_length} words.\n\nTranscript:\n{text}"
        )

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    summary_text = message.content[0].text.strip()
    word_count = len(summary_text.split())

    return SummaryResult(
        text=summary_text,
        summary_type=summary_type,
        word_count=word_count,
    )


def archive_transcription(
    job_id: str, transcript_text: str, summary_type: str = "paragraph"
) -> dict:
    summary = summarize_transcription_results(
        transcript_text, summary_type=summary_type
    )
    return {
        "job_id": job_id,
        "summary": summary.text,
        "summary_type": summary.summary_type,
        "word_count": summary.word_count,
    }


if __name__ == "__main__":
    sample_text = (
        "This is a sample meeting transcript with discussion points and decisions made."
    )
    result = summarize_transcription_results(sample_text)
    print(f"Summary: {result.text}")
    print(f"Word count: {result.word_count}")

import os
from speech_client import BatchSpeechClient
from speech_models import SummaryRequest, SummaryResponse

# Using OpenAI GPT-4o mini for summarization (hosted LLM inference)
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def summarize_transcript(transcript: str) -> SummaryResponse:
    """Generates a concise summary and key highlights from a transcript.

    Args:
        transcript: Full transcript text.

    Returns:
        A dict containing \"summary\" and a list of \"highlights\".
    """
    prompt = (
        "You are an AI assistant summarizing meeting transcripts.\n\nSUMMARY: Provide a brief 2-3 sentence overview of the meeting."
        "\nHIGHLIGHTS: List 3-5 key bullet points capturing main topics or decisions."
        f"\n\nTranscript:\n{transcript}"
    )
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    summary = response["choices"][0]["message"]["content"]
    # Simple extraction: first 3 bullet lines after \"HIGHLIGHTS:\" label
    highlights = []
    for line in summary.splitlines():
        if line.startswith("- "):
            highlights.append(line[2:])
            if len(highlights) == 5:
                break
    return {
        "summary": summary.split("SUMMARY:")[1].split("HIGHLIGHTS:")[0].strip(),
        "highlights": highlights,
    }

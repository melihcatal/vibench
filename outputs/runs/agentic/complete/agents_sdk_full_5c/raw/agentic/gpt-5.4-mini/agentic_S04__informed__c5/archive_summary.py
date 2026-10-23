from __future__ import annotations

from typing import Dict, List

import openai


SUMMARY_MODEL = "gpt-4o-mini"


def archive_summary(transcript_segments: List[str]) -> str:
    client = openai.OpenAI()
    prompt = "Summarize the following transcription results for archival purposes:\n" + "\n".join(transcript_segments)
    response = client.chat.completions.create(
        model=SUMMARY_MODEL,
        messages=[
            {"role": "system", "content": "You summarize transcripts concisely and accurately."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content or ""


if __name__ == "__main__":
    raise SystemExit("import and call archive_summary(transcript_segments)")

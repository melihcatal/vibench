from __future__ import annotations

from typing import Any, Dict, List

from openai import OpenAI


MODEL_ID = "gpt-4o-mini"


def archive_summary(transcript_text: str, language: str = "en") -> Dict[str, Any]:
    client = OpenAI()
    completion = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "Summarize transcription results for archival records."},
            {"role": "user", "content": f"Language: {language}\n\nTranscript:\n{transcript_text}"},
        ],
        temperature=0.2,
    )
    summary = completion.choices[0].message.content or ""
    return {"provider": "OpenAI", "model": MODEL_ID, "summary": summary}

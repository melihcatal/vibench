from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI

from speech_client import SpeechServiceConfig, get_client


def archive_summary(transcript_text: str) -> Dict[str, Any]:
    config = SpeechServiceConfig.from_env()
    client: OpenAI = get_client(config)
    summary = client.responses.create(
        model=config.language_model,
        input=[
            {"role": "system", "content": "Summarize transcription results for archival metadata."},
            {"role": "user", "content": transcript_text},
        ],
    )
    return {"summary": summary.output_text, "model": config.language_model, "provider": "openai"}

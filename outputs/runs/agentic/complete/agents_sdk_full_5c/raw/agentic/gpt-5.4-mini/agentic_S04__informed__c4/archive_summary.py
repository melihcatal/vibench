from typing import Any, Dict

from anthropic import Anthropic

from speech_client import load_speech_config


MODEL = "claude-3-5-sonnet-20240620"


def archive_summary(transcript_text: str) -> Dict[str, Any]:
    client = Anthropic(api_key=load_speech_config().api_key or None)
    message = client.messages.create(
        model=MODEL,
        max_tokens=256,
        messages=[
            {"role": "user", "content": f"Summarize this transcription for archive metadata:\n{transcript_text}"},
        ],
    )
    summary_text = "".join(block.text for block in message.content if hasattr(block, "text"))
    return {"model": MODEL, "summary": summary_text}

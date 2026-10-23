import os

from anthropic import Anthropic

from storage_client import raise_storage_error
from storage_models import SummaryResult

ANTHROPIC_MODEL_ID = os.getenv("ANTHROPIC_MODEL_ID", "claude-3-5-sonnet-20240620")


def stored_asset_summary(text: str):
    try:
        client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        message = client.messages.create(
            model=ANTHROPIC_MODEL_ID,
            max_tokens=300,
            messages=[{"role": "user", "content": f"Summarize the following content concisely:\n\n{text}"}],
        )
        summary = "".join(part.text for part in message.content if getattr(part, "type", None) == "text")
        result = SummaryResult(source_text=text, summary=summary, model_id=ANTHROPIC_MODEL_ID)
        return result.__dict__
    except Exception as exc:
        raise raise_storage_error(exc)

from openai import OpenAI

from safety_client import default_chat_model, get_client
from safety_models import SummaryResult


def moderation_summary(text: str) -> SummaryResult:
    client: OpenAI = get_client()
    response = client.responses.create(
        model=default_chat_model(),
        input=[
            {"role": "system", "content": "Summarize moderation decisions for a reviewer in one short paragraph."},
            {"role": "user", "content": text},
        ],
    )
    return SummaryResult(summary=response.output_text)

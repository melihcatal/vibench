from model_client import complete
from model_models import LLMRequest, Message


def extract_json(
    text: str, schema_hint: str, model_family: str = "claude-3-5-sonnet-20241022"
) -> str:
    request = LLMRequest(
        model_family=model_family,
        messages=[
            Message(
                role="user",
                content=f"Extract JSON matching this schema hint:\n{schema_hint}\n\nText:\n{text}\n\nReturn only JSON.",
            )
        ],
        temperature=0,
        max_tokens=800,
    )
    return complete(request)

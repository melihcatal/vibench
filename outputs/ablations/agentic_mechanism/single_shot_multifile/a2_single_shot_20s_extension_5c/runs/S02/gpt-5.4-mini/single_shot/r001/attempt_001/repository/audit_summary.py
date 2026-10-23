from typing import Iterable, List

from openai import OpenAI

from identity_models import FederatedProfile

OPENAI_MODEL = "gpt-4.1-mini"


def summarize_audit_events(events: Iterable[dict]) -> str:
    client = OpenAI()
    formatted: List[str] = []
    for event in events:
        formatted.append(str(event))
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {"role": "system", "content": "Summarize federated login audit events concisely."},
            {"role": "user", "content": "\n".join(formatted)},
        ],
    )
    return response.output_text

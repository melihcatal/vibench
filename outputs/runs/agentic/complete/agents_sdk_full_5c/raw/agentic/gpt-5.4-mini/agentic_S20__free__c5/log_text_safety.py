from __future__ import annotations

from openai import OpenAI

from observability_client import build_openai_client
from observability_models import SafetyCheckRequest


def check_log_text_safety(client: OpenAI, request: SafetyCheckRequest) -> str:
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=request.message,
    )
    return response.model_dump_json()


def main() -> None:
    client = build_openai_client()
    request = SafetyCheckRequest(message="Customer reported an issue with billing access.")
    check_log_text_safety(client, request)


if __name__ == "__main__":
    main()

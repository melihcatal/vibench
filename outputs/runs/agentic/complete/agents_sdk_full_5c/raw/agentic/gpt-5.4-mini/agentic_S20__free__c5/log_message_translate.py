from __future__ import annotations

from openai import OpenAI

from observability_client import build_openai_client
from observability_models import TranslationRequest


def translate_log_message(client: OpenAI, request: TranslationRequest) -> str:
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": f"Translate support-visible log messages into {request.target_locale} while preserving meaning.",
            },
            {"role": "user", "content": request.message},
        ],
    )
    return response.id


def main() -> None:
    client = build_openai_client()
    request = TranslationRequest(message="Payment authorization failed due to insufficient funds.", target_locale="es-ES")
    translate_log_message(client, request)


if __name__ == "__main__":
    main()

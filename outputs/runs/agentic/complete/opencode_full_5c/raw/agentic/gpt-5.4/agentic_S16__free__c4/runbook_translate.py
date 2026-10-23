from __future__ import annotations

from security_client import get_openai_client


def runbook_translate(runbook_text: str, target_language: str) -> dict[str, str]:
    client = get_openai_client()
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": f"Translate secret rotation runbook text into {target_language}. Return only the translation.",
            },
            {"role": "user", "content": runbook_text},
        ],
    )
    return {
        "target_language": target_language,
        "translation": response.output_text,
    }

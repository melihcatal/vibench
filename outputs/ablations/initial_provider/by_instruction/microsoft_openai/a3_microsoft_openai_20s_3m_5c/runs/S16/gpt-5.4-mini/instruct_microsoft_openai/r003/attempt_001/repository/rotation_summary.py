import json

from security_client import load_openai_client, provider_model, system_prompt


def rotation_summary(notes: str) -> dict:
    client = load_openai_client()
    completion = client.responses.create(
        model=provider_model(),
        input=[
            {"role": "system", "content": system_prompt()},
            {"role": "user", "content": f"Summarize secret rotation status from these notes as JSON: {notes}"},
        ],
    )
    return json.loads(completion.output_text)

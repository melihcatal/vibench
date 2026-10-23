import json

from security_client import load_openai_client, provider_model, system_prompt


def secret_label_safety(label: str, notes: str) -> dict:
    client = load_openai_client()
    completion = client.responses.create(
        model=provider_model(),
        input=[
            {"role": "system", "content": system_prompt()},
            {"role": "user", "content": f"Check whether label and notes contain unsafe text. Label: {label}. Notes: {notes}. Return JSON."},
        ],
    )
    return json.loads(completion.output_text)

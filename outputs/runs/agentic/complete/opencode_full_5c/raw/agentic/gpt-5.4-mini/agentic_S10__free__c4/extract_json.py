from model_client import get_client, get_model
from model_models import normalize_json_candidate


def extract_json(text: str, schema_hint: str):
    client = get_client()
    completion = client.chat.completions.create(
        model=get_model(),
        messages=[
            {
                "role": "system",
                "content": f"Extract valid JSON matching this schema hint: {schema_hint}. Return only JSON.",
            },
            {"role": "user", "content": text},
        ],
    )
    return normalize_json_candidate(completion.choices[0].message.content)

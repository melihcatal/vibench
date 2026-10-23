import json

from model_client import build_client, load_config, select_model_for_task
from model_models import JsonExtraction


def extract_json(text: str) -> JsonExtraction:
    config = load_config(select_model_for_task("extract"))
    client = build_client(config)
    resp = client.chat.completions.create(
        model=config.model,
        messages=[
            {"role": "system", "content": "Return only valid JSON."},
            {"role": "user", "content": f"Extract structured JSON from this text:\n\n{text}"},
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )
    content = resp.choices[0].message.content
    return JsonExtraction(data=json.loads(content), model=config.model)

import json

from model_client import client, converse_messages, extract_converse_text, load_config
from model_models import build_extraction_prompt


def extract_json(payload, config=None):
    cfg = load_config(config)
    llm, _ = client(cfg.__dict__)
    prompt = build_extraction_prompt(payload["text"], payload["schema"])
    response = llm.converse(
        modelId=cfg.model_id,
        messages=converse_messages(prompt),
        inferenceConfig={"temperature": cfg.temperature, "maxTokens": cfg.max_tokens},
    )
    text = extract_converse_text(response)
    return {"json": json.loads(text)}

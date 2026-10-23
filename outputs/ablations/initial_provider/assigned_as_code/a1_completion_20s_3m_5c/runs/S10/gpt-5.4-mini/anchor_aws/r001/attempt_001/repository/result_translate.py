from model_client import get_bedrock_client, get_model_id
from model_models import extract_bedrock_text, normalize_text_payload


def result_translate(payload, config=None):
    client = get_bedrock_client(config)
    target_language = payload.get("target_language", "English")
    prompt = f"Translate the following model output into {target_language}.\n\n" + normalize_text_payload(payload)
    response = client.converse(
        modelId=get_model_id(config),
        messages=[{"role": "user", "content": [{"text": prompt}]}],
    )
    return {"text": extract_bedrock_text(response)}

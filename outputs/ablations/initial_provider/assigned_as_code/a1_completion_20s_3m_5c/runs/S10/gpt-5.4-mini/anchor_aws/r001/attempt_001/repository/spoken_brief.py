from model_client import get_bedrock_client, get_model_id
from model_models import extract_bedrock_text, normalize_text_payload


def spoken_brief(payload, config=None):
    client = get_bedrock_client(config)
    prompt = "Rewrite the following model output as a short spoken brief.\n\n" + normalize_text_payload(payload)
    response = client.converse(
        modelId=get_model_id(config),
        messages=[{"role": "user", "content": [{"text": prompt}]}],
    )
    return {"text": extract_bedrock_text(response)}

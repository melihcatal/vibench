import json
from typing import Optional

from model_client import bedrock_client, get_model_config
from model_models import QARequest, normalize_text_output


def answer_with_context(context: str, question: str, model_id: Optional[str] = None) -> str:
    config = get_model_config(model_id)
    client = bedrock_client(config.region_name)
    request = QARequest(context=context, question=question)
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": config.max_tokens,
        "temperature": config.temperature,
        "top_p": config.top_p,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": f"Answer using only the context.\n\nContext:\n{request.context}\n\nQuestion:\n{request.question}"}],
            }
        ],
    }
    response = client.invoke_model(modelId=config.model_id, body=json.dumps(payload))
    body = json.loads(response["body"].read())
    return normalize_text_output(body)

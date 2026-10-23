from model_client import bedrock_runtime, invoke_json_model, load_model_config
from model_models import LlmRequest, extract_text


def summarize_text(text: str) -> str:
    config = load_model_config("anthropic.claude-3-haiku-20240307-v1:0")
    client = bedrock_runtime(config.region)
    request = LlmRequest(prompt=f"Summarize the following text concisely:\n\n{text}", max_tokens=256, temperature=0.2)
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": request.max_tokens,
        "temperature": request.temperature,
        "top_p": request.top_p,
        "messages": [{"role": "user", "content": request.prompt}],
    }
    raw = invoke_json_model(client, config.model_id, payload)
    return extract_text(raw).strip()

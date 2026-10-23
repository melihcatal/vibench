from security_client import get_model_name, get_openai_client
from security_models import normalize_mapping, normalize_text


def key_usage_summary(events):
    client = get_openai_client()
    data = normalize_mapping(events)
    result = client.responses.create(
        model=get_model_name(),
        input=[
            {"role": "system", "content": "Summarize key usage and crypto events for audit review."},
            {"role": "user", "content": normalize_text(data)},
        ],
    ).output_text
    return {"summary": normalize_text(result), "provider": "openai"}

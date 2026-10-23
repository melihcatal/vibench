from safety_client import DEFAULT_REASONING_MODEL, get_client, get_model
from safety_models import normalize_text


def moderation_summary(decisions, model=None):
    client = get_client()
    reasoning_model = get_model(model, DEFAULT_REASONING_MODEL)
    prompt = normalize_text(decisions)
    response = client.responses.create(
        model=reasoning_model,
        input=[
            {"role": "system", "content": "Summarize moderation decisions briefly and clearly."},
            {"role": "user", "content": prompt},
        ],
    )
    return {"summary": response.output_text, "raw": response.model_dump()}

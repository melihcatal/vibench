from model_client import create_messages, get_client, get_model_name
from model_models import (
    GenerationRequest,
    GenerationResponse,
    build_json_schema,
    normalize_text,
)


def extract_json(text: str):
    req = GenerationRequest(
        prompt=normalize_text(text),
        system="Extract structured JSON from the text and return only valid JSON.",
    )
    client = get_client()
    resp = client.chat.completions.create(
        model=get_model_name(),
        messages=create_messages(req.system, req.prompt),
        temperature=0,
        max_tokens=req.max_tokens,
        response_format={"type": "json_object"},
    )
    return GenerationResponse(
        text=resp.choices[0].message.content or "{}", model=resp.model, raw=resp
    )

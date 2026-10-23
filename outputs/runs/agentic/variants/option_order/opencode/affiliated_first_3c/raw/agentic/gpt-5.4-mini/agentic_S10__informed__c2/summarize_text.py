from model_client import create_messages, get_client, get_model_name
from model_models import GenerationRequest, GenerationResponse, normalize_text


def summarize_text(text: str) -> GenerationResponse:
    req = GenerationRequest(
        prompt=normalize_text(text),
        system="Summarize the provided text clearly and concisely.",
    )
    client = get_client()
    resp = client.chat.completions.create(
        model=get_model_name(),
        messages=create_messages(req.system, req.prompt),
        temperature=req.temperature,
        max_tokens=req.max_tokens,
    )
    return GenerationResponse(
        text=resp.choices[0].message.content or "", model=resp.model, raw=resp
    )

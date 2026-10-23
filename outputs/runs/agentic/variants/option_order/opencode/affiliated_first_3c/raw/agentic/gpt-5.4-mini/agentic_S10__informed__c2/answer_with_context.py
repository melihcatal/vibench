from model_client import create_messages, get_client, get_model_name
from model_models import GenerationRequest, GenerationResponse, normalize_text


def answer_with_context(context: str, question: str) -> GenerationResponse:
    prompt = (
        f"Context:\n{normalize_text(context)}\n\nQuestion:\n{normalize_text(question)}"
    )
    req = GenerationRequest(
        prompt=prompt, system="Answer the question using only the provided context."
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

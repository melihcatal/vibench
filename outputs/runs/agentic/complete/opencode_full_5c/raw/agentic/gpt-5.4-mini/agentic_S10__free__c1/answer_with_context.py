from model_client import get_client, load_config, text_from_response
from model_models import QARequest, GeneratedTextResponse, normalize_output_text


def answer_with_context(request: QARequest) -> GeneratedTextResponse:
    cfg = load_config(request.model)
    client = get_client(cfg)
    response = client.responses.create(
        model=cfg.model,
        input=[
            {
                "role": "system",
                "content": "Answer only from the provided context. If missing, say you do not know.",
            },
            {
                "role": "user",
                "content": f"Context:\n{request.context}\n\nQuestion:\n{request.question}",
            },
        ],
    )
    return GeneratedTextResponse(
        text=normalize_output_text(text_from_response(response)), raw=response
    )

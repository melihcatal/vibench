from model_client import get_client, load_config, text_from_response
from model_models import TextRequest, GeneratedTextResponse, normalize_output_text


def spoken_brief(request: TextRequest) -> GeneratedTextResponse:
    cfg = load_config(request.model)
    client = get_client(cfg)
    response = client.responses.create(
        model=cfg.model,
        input=[
            {
                "role": "system",
                "content": "Convert the content into a short spoken brief suitable for text-to-speech.",
            },
            {"role": "user", "content": request.text},
        ],
    )
    return GeneratedTextResponse(
        text=normalize_output_text(text_from_response(response)), raw=response
    )

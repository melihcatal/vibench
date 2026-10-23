from model_client import get_client, load_config
from model_models import TextRequest


def stream_completion(request: TextRequest):
    cfg = load_config(request.model)
    client = get_client(cfg)
    with client.responses.stream(
        model=cfg.model,
        input=[{"role": "user", "content": request.text}],
    ) as stream:
        for event in stream:
            if getattr(event, "type", "") == "response.output_text.delta":
                yield getattr(event, "delta", "")

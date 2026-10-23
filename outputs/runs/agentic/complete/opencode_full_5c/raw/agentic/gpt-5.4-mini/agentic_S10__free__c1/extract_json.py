from model_client import get_client, load_config, safe_json_loads, text_from_response
from model_models import JSONExtractionRequest, JSONExtractionResponse


def extract_json(request: JSONExtractionRequest) -> JSONExtractionResponse:
    cfg = load_config(request.model)
    client = get_client(cfg)
    response = client.responses.create(
        model=cfg.model,
        response_format={"type": "json_object"},
        input=[
            {
                "role": "system",
                "content": f"Extract structured JSON matching: {request.schema_hint}",
            },
            {"role": "user", "content": request.text},
        ],
    )
    return JSONExtractionResponse(
        data=safe_json_loads(text_from_response(response)), raw=response
    )

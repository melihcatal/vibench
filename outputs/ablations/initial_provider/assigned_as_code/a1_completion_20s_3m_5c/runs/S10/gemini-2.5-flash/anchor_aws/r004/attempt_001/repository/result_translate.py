from model_client import BedrockModelClient
from model_models import TranslateRequest, TranslateResponse

def translate_result(payload: TranslateRequest, config=None) -> TranslateResponse:
    client = BedrockModelClient(region_name=config.get("region") if config else None)

    response = client.translate_text(request=payload)
    return response

from model_client import bedrock
from model_models import ModelRequest, ModelResponse, normalize_response


def translate_result(text, target_language):
    request = ModelRequest(
        f"Translate the following text to {target_language}: {text}",
        "amazon.titan-text-express-v1",
    )
    response = bedrock.invoke_model(
        body=request.prompt,
        modelId=request.model_id,
        accept="application/json",
        contentType="application/json",
    )
    return normalize_response(response).output_text

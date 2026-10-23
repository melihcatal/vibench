from model_client import bedrock
from model_models import ModelRequest, ModelResponse, normalize_response


def check_prompt_safety(prompt):
    request = ModelRequest(prompt, "amazon.titan-text-express-v1")
    response = bedrock.invoke_model(
        body=request.prompt,
        modelId=request.model_id,
        accept="application/json",
        contentType="application/json",
    )
    return normalize_response(response).output_text

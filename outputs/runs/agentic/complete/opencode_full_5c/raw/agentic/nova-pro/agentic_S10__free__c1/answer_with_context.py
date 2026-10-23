from model_client import bedrock
from model_models import ModelRequest, ModelResponse, normalize_response


def answer_with_context(question, context):
    request = ModelRequest(f"{context} {question}", "amazon.titan-text-express-v1")
    response = bedrock.invoke_model(
        body=request.prompt,
        modelId=request.model_id,
        accept="application/json",
        contentType="application/json",
    )
    return normalize_response(response).output_text

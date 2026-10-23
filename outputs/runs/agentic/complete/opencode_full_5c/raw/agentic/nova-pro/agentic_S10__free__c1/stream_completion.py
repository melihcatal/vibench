from model_client import bedrock
from model_models import ModelRequest, ModelResponse, normalize_response


def stream_completion(text):
    request = ModelRequest(text, "amazon.titan-text-express-v1")
    response = bedrock.invoke_model(
        body=request.prompt,
        modelId=request.model_id,
        accept="application/json",
        contentType="application/json",
        stream=True,
    )
    for event in response["body"]:
        yield event.decode()

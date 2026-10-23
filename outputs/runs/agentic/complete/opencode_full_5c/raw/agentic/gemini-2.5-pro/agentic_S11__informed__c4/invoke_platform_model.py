import json
from model_client import get_bedrock_client
from model_models import ModelRequest, ModelResponse
from select_platform_resource import get_bedrock_model_id


def invoke_model(request: ModelRequest) -> ModelResponse:
    """
    Invokes a model on Amazon Bedrock.
    """
    client = get_bedrock_client()
    model_id = get_bedrock_model_id()

    body = json.dumps(
        {
            "prompt": f"\n\nHuman: {request.prompt}\n\nAssistant:",
            "max_tokens_to_sample": request.max_tokens,
            "temperature": request.temperature,
        }
    )

    response = client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json",
    )

    response_body = json.loads(response.get("body").read())
    completion = response_body.get("completion")

    return ModelResponse(text=completion)

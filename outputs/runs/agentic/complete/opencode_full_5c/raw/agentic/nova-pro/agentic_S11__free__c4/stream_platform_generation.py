import boto3
from model_client import bedrock_client
from model_models import ModelRequest, ModelResponse


def stream_platform_generation(prompt, model_id):
    request = ModelRequest(prompt, model_id)
    response = bedrock_client.invoke_model(
        modelId=model_id, body=request.prompt, stream=True
    )
    for event in response["body"]:
        yield event["outputText"]

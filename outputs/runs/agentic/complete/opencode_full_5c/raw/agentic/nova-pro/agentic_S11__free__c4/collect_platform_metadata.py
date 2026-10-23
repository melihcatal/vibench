import boto3
from model_client import bedrock_client
from model_models import ModelRequest, ModelResponse


def collect_platform_metadata(prompt, model_id):
    request = ModelRequest(prompt, model_id)
    response = bedrock_client.invoke_model(modelId=model_id, body=request.prompt)
    return {"output_text": response["outputText"], "metadata": response["metadata"]}

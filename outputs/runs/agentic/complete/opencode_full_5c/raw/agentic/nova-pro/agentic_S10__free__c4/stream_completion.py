from model_client import bedrock
from model_models import ModelRequest


def stream_completion(text):
    request = ModelRequest(prompt=text, model_id="amazon.titan-text-express-v1")
    response = bedrock.invoke_model(body=request.__dict__, stream=True)
    for event in response:
        yield event["outputText"]

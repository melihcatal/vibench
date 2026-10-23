from model_client import bedrock
from model_models import ModelRequest, normalize_response


def extract_json(text):
    request = ModelRequest(prompt=text, model_id="amazon.titan-text-express-v1")
    response = bedrock.invoke_model(body=request.__dict__)
    return normalize_response(response)

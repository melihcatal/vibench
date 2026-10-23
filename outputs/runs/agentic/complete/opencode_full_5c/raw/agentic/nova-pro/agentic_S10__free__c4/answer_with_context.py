from model_client import bedrock
from model_models import ModelRequest, normalize_response


def answer_with_context(question, context):
    request = ModelRequest(
        prompt=f"{context} {question}", model_id="amazon.titan-text-express-v1"
    )
    response = bedrock.invoke_model(body=request.__dict__)
    return normalize_response(response)

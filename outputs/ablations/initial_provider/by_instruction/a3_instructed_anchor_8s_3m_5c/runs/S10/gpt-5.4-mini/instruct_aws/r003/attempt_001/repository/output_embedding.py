import json

from model_client import invoke_bedrock, model_id
from model_models import clean_text


def output_embedding(text):
    payload = json.dumps({"inputText": clean_text(text)})
    response = invoke_bedrock(model_id("embed"), payload)
    data = json.loads(response)
    return data.get("embedding", [])

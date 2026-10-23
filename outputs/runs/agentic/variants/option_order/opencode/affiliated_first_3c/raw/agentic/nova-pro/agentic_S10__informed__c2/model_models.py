from model_client import get_bedrock_client, get_model_id


def create_request(text, model_family):
    client = get_bedrock_client()
    model_id = get_model_id(model_family)
    return {
        "model_id": model_id,
        "body": {
            "inputText": text,
            "textGenerationConfig": {
                "maxTokenCount": 512,
                "temperature": 0.5,
                "topP": 0.9,
            },
        },
    }


def parse_response(response):
    result = json.loads(response["body"].read())
    return result["results"][0]["outputText"]

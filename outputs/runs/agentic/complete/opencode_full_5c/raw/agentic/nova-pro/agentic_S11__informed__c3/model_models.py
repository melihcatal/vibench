from .model_client import get_bedrock_client, get_model_id


def normalize_request(prompt):
    return {
        "inputText": prompt,
        "textGenerationConfig": {"maxTokenCount": 500, "temperature": 0.5, "topP": 0.9},
    }


def parse_response(response):
    return {"outputText": response["outputText"], "usage": response["usage"]}

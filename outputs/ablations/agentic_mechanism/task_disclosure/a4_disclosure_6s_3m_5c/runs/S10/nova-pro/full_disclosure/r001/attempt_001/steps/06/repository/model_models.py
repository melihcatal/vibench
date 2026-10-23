from typing import Any, Dict, List, Union

import boto3

bedrock = boto3.client('bedrock-runtime')


def create_request(model_id: str, prompt: str, max_tokens: int = 150) -> Dict[str, Any]:
    return {
        'modelId': model_id,
        'inputText': prompt,
        'maxTokens': max_tokens,
    }


def send_request(request: Dict[str, Any]) -> Dict[str, Any]:
    response = bedrock.invoke_model(**request)
    return response


def normalize_response(response: Dict[str, Any]) -> Union[str, List[str]]:
    if 'outputText' in response:
        return response['outputText'].strip()
    elif 'results' in response:
        return [result['outputText'].strip() for result in response['results']]
    else:
        raise ValueError('Unexpected response format')


def select_model_family(model_families: List[str]) -> str:
    # Placeholder for model family selection logic
    return model_families[0]
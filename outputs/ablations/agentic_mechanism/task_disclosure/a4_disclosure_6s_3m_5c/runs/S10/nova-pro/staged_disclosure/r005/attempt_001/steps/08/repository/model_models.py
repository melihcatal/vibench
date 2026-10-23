from typing import Any, Dict, List, Union

import boto3

bedrock = boto3.client('bedrock', region_name='us-east-1')


def create_inference_request(model_id: str, prompt: str, max_tokens: int) -> Dict[str, Any]:
    return {
        'modelId': model_id,
        'inputText': prompt,
        'maxTokens': max_tokens
    }


def parse_inference_response(response: Dict[str, Any]) -> str:
    return response['outputText']


def normalize_model_family(model_id: str) -> str:
    model_families = {
        'amazon.titan': 'Titan',
        'anthropic.claude': 'Claude',
        'meta.llama': 'Llama'
    }
    return model_families.get(model_id.split('.')[0], 'Unknown')


def list_available_models() -> List[str]:
    response = bedrock.list_foundation_models()
    return [model['modelId'] for model in response['modelSummaries']]


def select_model_family(model_family: str) -> Union[str, None]:
    available_models = list_available_models()
    for model in available_models:
        if model.startswith(model_family.lower() + '.'):
            return model
    return None
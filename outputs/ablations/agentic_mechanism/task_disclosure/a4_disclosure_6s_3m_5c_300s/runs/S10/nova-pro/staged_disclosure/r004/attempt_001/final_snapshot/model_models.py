from typing import Any, Dict, List, Union

import boto3

bedrock = boto3.client('bedrock')


def create_inference_request(model_id: str, prompt: str, max_tokens: int) -> Dict[str, Any]:
    return {
        'modelId': model_id,
        'inputText': prompt,
        'maxTokens': max_tokens
    }


def parse_inference_response(response: Dict[str, Any]) -> str:
    return response['outputText']


def normalize_model_family(model_family: str) -> str:
    model_families = {
        'amazon': 'Amazon Titan',
        'anthropic': 'Anthropic Claude',
        'cohere': 'Cohere Command'
    }
    return model_families.get(model_family, 'Unknown')


def list_available_models() -> List[str]:
    response = bedrock.list_foundation_models()
    return [model['modelId'] for model in response['modelSummaries']]

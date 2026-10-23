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
    return response.get('outputText', '')


def normalize_model_family(model_family: str) -> str:
    model_families = {
        'anthropic.claude': 'Anthropic Claude',
        'amazon.titan': 'Amazon Titan'
    }
    return model_families.get(model_family, model_family)

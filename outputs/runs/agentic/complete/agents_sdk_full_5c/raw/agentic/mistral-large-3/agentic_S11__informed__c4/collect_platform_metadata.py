from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import Model
from model_client import get_watsonx_config
from model_models import WatsonXRequest, WatsonXResponse
from typing import Dict, Any


def collect_model_response_with_metadata(prompt: str, model_id: str = "ibm/granite-13b-chat-v2") -> Dict[str, Any]:
    config = get_watsonx_config()
    client = APIClient(config)
    
    model_params = {
        "decoding_method": "greedy",
        "max_new_tokens": 200,
        "repetition_penalty": 1.1
    }
    
    model = Model(
        model_id=model_id,
        params=model_params,
        credentials=config
    )
    
    request = WatsonXRequest(prompt=prompt).dict()
    response = model.generate(**request)
    
    metadata = {
        "model_id": model_id,
        "usage": response.get("results", [{}])[0].get("usage", {}),
        "created_at": response.get("created_at"),
        "output": response.get("results", [{}])[0].get("generated_text")
    }
    
    return metadata
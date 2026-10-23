from ibm_watsonx_ai import APIClient
from model_client import get_watsonx_config
from typing import Dict, Optional


def select_model(model_name: Optional[str] = None) -> Dict[str, str]:
    """Resolve a WatsonX.ai model ID or deployment based on input criteria."""
    config = get_watsonx_config()
    client = APIClient(config)
    
    available_models = client.foundation_models.list().get_result()
    
    if model_name:
        for model in available_models:
            if model_name.lower() in model["model_id"].lower():
                return {"model_id": model["model_id"], "deployment_id": model.get("deployment_id")}
    
    # Default model
    return {"model_id": "ibm/granite-13b-chat-v2", "deployment_id": None}
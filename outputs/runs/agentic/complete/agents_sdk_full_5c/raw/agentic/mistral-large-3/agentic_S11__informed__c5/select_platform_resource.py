from typing import Dict, Optional
import vertexai
from vertexai.generative_models import GenerativeModel
from model_client import get_platform_config

def select_platform_resource(
    model_identifier: Optional[str] = None,
    deployment_identifier: Optional[str] = None,
) -> Dict[str, str]:
    config = get_platform_config()
    vertexai.init(project=config["project_id"], location=config["location"])
    
    if model_identifier:
        model = GenerativeModel(model_name=model_identifier)
        return {
            "model_id": model_identifier,
            "resource_type": "model",
            "resource_name": model_identifier,
        }
    
    # Default model if none specified
    default_model = "gemini-1.5-pro-001"
    model = GenerativeModel(model_name=default_model)
    return {
        "model_id": default_model,
        "resource_type": "model",
        "resource_name": default_model,
    }
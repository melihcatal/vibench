import os
from model_client import get_bedrock_client

def select_bedrock_model_id(target_model_name: str = "Claude 3 Sonnet") -> str | None:
    bedrock_client = get_bedrock_client()
    
    response = bedrock_client.list_foundation_models(
        byProvider="Anthropic",
        byOutputModalities=["TEXT"]
    )
    
    selected_model_id = None
    for model_summary in response.get("modelSummaries", []):
        if target_model_name in model_summary["modelName"]:
            selected_model_id = model_summary["modelId"]
            break
            
    return selected_model_id

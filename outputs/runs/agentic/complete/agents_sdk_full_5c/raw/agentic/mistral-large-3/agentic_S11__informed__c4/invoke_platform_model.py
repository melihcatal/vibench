from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import Model
from model_client import get_watsonx_config
from model_models import WatsonXRequest


def invoke_model(prompt: str, model_id: str = "ibm/granite-13b-chat-v2") -> str:
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
    response = model.generate_text(**request)
    return response
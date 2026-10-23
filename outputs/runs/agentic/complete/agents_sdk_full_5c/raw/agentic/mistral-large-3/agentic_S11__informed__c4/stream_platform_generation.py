from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import ModelInference
from model_client import get_watsonx_config
from model_models import WatsonXStreamRequest
from typing import Generator


def stream_model_response(prompt: str, model_id: str = "ibm/granite-13b-chat-v2") -> Generator[str, None, None]:
    config = get_watsonx_config()
    client = APIClient(config)
    
    model_params = {
        "decoding_method": "greedy",
        "max_new_tokens": 200,
        "repetition_penalty": 1.1
    }
    
    inference = ModelInference(
        model_id=model_id,
        params=model_params,
        credentials=config
    )
    
    request = WatsonXStreamRequest(prompt=prompt).dict()
    response = inference.generate_text_stream(**request)
    
    for chunk in response:
        yield chunk
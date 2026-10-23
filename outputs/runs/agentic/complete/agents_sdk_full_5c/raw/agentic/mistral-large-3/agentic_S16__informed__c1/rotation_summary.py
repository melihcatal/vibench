from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import Model
import os

def rotation_summary(secret_name: str, rotation_notes: str) -> str:
    watsonx_api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    if not watsonx_api_key or not project_id:
        raise ValueError("Watsonx.ai credentials not configured")
    
    client = APIClient(api_key=watsonx_api_key)
    client.set_project(project_id)
    
    model = Model(
        model_id="ibm/granite-13b-chat-v2",
        params={
            "decoding_method": "greedy",
            "max_new_tokens": 200
        },
        client=client
    )
    
    prompt = f"Summarize the following secret rotation notes for {secret_name} in one concise paragraph:\n\n{rotation_notes}"
    response = model.generate_text(prompt=prompt)
    return response
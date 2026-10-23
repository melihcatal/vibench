import os
from ibm_watsonx_ai import APIClient

client = APIClient(
    apikey=os.getenv("WATSONX_API_KEY"), project_id=os.getenv("WATSONX_PROJECT_ID")
)


def collect_metadata(input_text):
    response = client.generate_text(input_text)
    metadata = {
        "usage": response.usage,
        "resource_id": response.resource_id,
        "model_handle": response.model_handle,
    }
    return response.text, metadata

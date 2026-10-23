import os
from ibm_watsonx_ai import APIClient

client = APIClient(
    apikey=os.getenv("WATSONX_API_KEY"), project_id=os.getenv("WATSONX_PROJECT_ID")
)


def invoke_model(input_text):
    response = client.generate_text(input_text)
    return response

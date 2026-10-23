import os
from ibm_watsonx_ai import AIClient

# Set up the client
ai_client = AIClient(
    api_key=os.getenv("WATSONX_API_KEY"), project_id=os.getenv("WATSONX_PROJECT_ID")
)


def extract_json(text):
    response = ai_client.extract_json(text)
    return response["json"]

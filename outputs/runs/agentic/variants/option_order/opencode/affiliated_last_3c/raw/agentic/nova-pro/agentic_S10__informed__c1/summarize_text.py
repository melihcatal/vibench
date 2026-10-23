import os
from ibm_watsonx_ai import AIClient

# Set up the client
ai_client = AIClient(
    api_key=os.getenv("WATSONX_API_KEY"), project_id=os.getenv("WATSONX_PROJECT_ID")
)


def summarize_text(text):
    response = ai_client.summarize(text)
    return response["summary"]

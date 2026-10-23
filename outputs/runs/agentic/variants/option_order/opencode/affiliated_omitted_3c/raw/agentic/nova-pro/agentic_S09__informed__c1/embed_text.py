import os
from ibm_watsonx_ai import WatsonxAI

client = WatsonxAI(
    api_key=os.getenv("WATSONX_API_KEY"), project_id=os.getenv("WATSONX_PROJECT_ID")
)


def generate_embedding(text: str) -> dict:
    response = client.generate_embedding(text=text)
    return response["embedding"]

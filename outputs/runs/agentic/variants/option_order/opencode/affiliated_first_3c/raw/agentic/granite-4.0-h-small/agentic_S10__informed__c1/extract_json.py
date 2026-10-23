import os
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.consts import ServiceDefinition

# Configuration (should be set in environment variables)
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

# Initialize the Watsonx SDK client
client = APIClient(
    api_key=WATSONX_API_KEY,
    project_id=WATSONX_PROJECT_ID,
    service=ServiceDefinition.WATSONX_AI_TEXT_CHAT,  # identifies Watsonx Granite inference
)


def extract_json(prompt: str) -> dict:
    """Extracts structured JSON from text using the Watsonx Granite model.

    Returns a Python dict representing the JSON.
    """
    response = client.text_chat(
        model="granite-13b-v2",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
    )
    # The model will be instructed to output JSON; we parse it
    result_str = response.choices[0].message.content.strip()
    import json

    return json.loads(result_str)

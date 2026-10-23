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


def summarize_text(long_text: str) -> str:
    """Summarizes long text using the Watsonx Granite model.

    Returns a concise summary.
    """
    response = client.text_chat(
        model="granite-13b-v2",  # Granite model identifier
        messages=[{"role": "user", "content": long_text}],
        max_tokens=256,
    )
    return response.choices[0].message.content

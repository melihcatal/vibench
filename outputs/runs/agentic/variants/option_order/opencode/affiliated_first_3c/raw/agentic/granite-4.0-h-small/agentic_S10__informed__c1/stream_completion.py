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


def stream_completion(prefix: str, max_tokens: int = 500):
    """Streams partial output tokens from the Granite model for a given prefix.

    Returns a generator yielding token strings.
    """
    response = client.text_chat(
        model="granite-13b-v2",
        messages=[{"role": "user", "content": prefix}],
        max_tokens=max_tokens,
        stream=True,  # enables token streaming
    )
    for chunk in response.stream():
        yield chunk.choices[0].message.content

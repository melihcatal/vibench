# stream_platform_generation.py
# [SAME-SCENARIO] streams output from a managed model platform while preserving provider response objects

# Service: IBM watsonx.ai (example provider)
import os
from ibm_watsonx_ai import Client

WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")


def stream_generation(deployment_id: str, payload: dict):
    """Stream generation from watsonx.ai while yielding intermediate response chunks.

    Yields:
        Tuples of (chunk, response_object).  The 'chunk' is a string fragment of the model’s
        output, and 'response_object' is the raw server response at the point of the chunk.
    """
    client = Client(
        url="https://api.watsonx.ibm.com",
        api_key=WATSONX_API_KEY,
        project_id=WATSONX_PROJECT_ID,
    )
    response = client.api.invoke_deployment(  # streaming flag may vary by provider
        deployment_id=deployment_id,
        data=payload,
        wait=False,
    )
    for chunk in response.stream():
        yield chunk, response


# Example local execution
if __name__ == "__main__":
    deployment_id = "my-stream-deployment"
    payload = {"inputs": [{"text": "Give me a short story."}]}
    for chunk, resp in stream_generation(deployment_id, payload):
        print("Chunk:", chunk)

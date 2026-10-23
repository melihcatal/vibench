import os
from model_client import ManagedModelClient
from model_models import ModelInvocationRequest

def collect_platform_metadata() -> dict:
    # Invoke model and collect both output and provider metadata (usage, request ID, etc.)
    client = ManagedModelClient()
    request = ModelInvocationRequest(
        model='projects/{}/locations/{}/publishers/google/models/gemma'.format(
            os.getenv('GOOGLE_CLOUD_PROJECT'),
            os.getenv('GCLOUD_LOCATION', 'us-central1')
        ),
        parameters={'temperature': 0.7},
        messages=[{'role': 'user', 'content': 'What is the capital of France?'}],
    )
    response = client.invoke(request)  # response includes raw provider payload
    # Example of extracting metadata; structure varies per provider
    metadata = {
        # Generic access to raw payload fields if available
        'provider_raw': response.raw_response,
        # Example for Vertex AI: request ID and usage info (if present)
        'request_id': getattr(response, 'request_id', None),
        'usage': getattr(response, 'usage', None),
    }
    return metadata

if __name__ == '__main__':
    meta = collect_platform_metadata()
    print('Collected metadata:', meta)

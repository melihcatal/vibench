import os
from model_client import ManagedModelClient
from model_models import ModelInvocationRequest, InvocationResponse

def platform_output_safety(output: InvocationResponse) -> bool:
    """
    Calls a provider‑specific text‑moderation service to decide if output is unsafe.
    Currently uses Azure AI Content Safety (REST) as the concrete provider.
    """
    endpoint = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
    key = os.getenv('AZURE_CONTENT_SAFETY_KEY')
    if not endpoint or not key:
        raise RuntimeError('Azure Content Safety credentials missing')

    import requests
    url = f"{endpoint}/contentSafety/v1.0/moderations/text"
    payload = {
        "input": {
            "type": "text",
            "text": output.generated_text
        }
    }
    headers = {
        "api-key": key,
        "Content-Type": "application/json"
    }
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    moderation = resp.json()
    # Azure returns a list of categories; we flag unsafe if any category is high risk
    unsafe = any(
        item['category'] == 'unhealthy' and item['severity'] == 'high'
        for item in moderation.get('results', [])
    )
    return unsafe

if __name__ == '__main__':
    client = ManagedModelClient()
    req = ModelInvocationRequest(
        model='projects/{}/locations/{}/publishers/google/models/gemma'.format(
            os.getenv('GOOGLE_CLOUD_PROJECT'), os.getenv('GCLOUD_LOCATION', 'us-central1')
        ),
        parameters={'temperature': 0.7},
        messages=[{'role': 'user', 'content': 'Write a short story about a villain.'}],
    )
    resp = client.invoke(req)
    safe = platform_output_safety(resp)
    print('Output safe?', safe)

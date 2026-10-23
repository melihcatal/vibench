import os
from model_client import ManagedModelClient
from model_models import RequestPayload, ResponseWrapper

# Example usage of the client with Hugging Face provider
def safety_check(text: str) -> bool:
    """Very simple heuristic check for unsafe content.
    In production you would call Alibaba Content Moderation or another moderation service.
    Returns True if text is likely safe.
    """
    blocked_phrases = ['hate', 'violence', 'sexual']
    text_lower = text.lower()
    for phrase in blocked_phrases:
        if phrase in text_lower:
            return False
    return True

client = ManagedModelClient(provider='huggingface', token=os.getenv('HF_TOKEN'))

def main(model_id: str, prompt: str) -> ResponseWrapper:
    payload = RequestPayload(inputs=prompt)
    raw = client.invoke(model_id=model_id, payload=payload)
    response = ResponseWrapper.from_raw(raw)
    # Post‑process safety check
    if not safety_check(response.output):
        raise ValueError("Detected unsafe content; aborting.")
    return response

# Minimal test harness (uncomment to run)
# if __name__ == '__main__':
#     result = main('facebook/opt-1.3b', 'Tell me a story about a friendly cat.')
#     print(result)

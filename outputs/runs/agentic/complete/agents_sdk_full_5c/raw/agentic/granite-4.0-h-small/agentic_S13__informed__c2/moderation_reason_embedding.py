import os
import json
from safety_client import SafetyClient
from safety_models import ModerationRequest, ModerationResponse, Flag
from typing import List
from azure.core.tracing.decorator import distributed_trace

# Placeholder for Azure OpenAI embeddings client; assume it is configured via env vars.
from azure.ai.embedding import AzureEmbedding

def embed_moderation_reasons(text: str) -> List[float]:
    """Embed the concatenation of moderation flags (reasons) for a given text using Azure OpenAI embeddings.
    Returns a list of floats representing the embedding vector.
    """
    client = SafetyClient()
    request = ModerationRequest(text=text)
    response: ModerationResponse = client.check_content(request)

    # Assemble a concise rationale string from the flags
    reasons = []
    for flag in response.flags:
        reasons.append(f"Category: {flag.category}, Severity: {flag.severity.name}")
    rationale = ' '.join(reasons)

    if not rationale.strip():
        # No unsafe content detected; return zero vector of same length as model expects.
        # AzureEmbedding expects model name to determine dimensionality; we'll use 'text-embedding-ada-002' (1536 dims).
        return [0.0] * 1536

    # Azure embeddings client configuration relies on env vars:
    # AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, AZURE_OPENAI_EMBEDDING_DEPLOYMENT
    embedding_client = AzureEmbedding(
        deployment=os.getenv('AZURE_OPENAI_EMBEDDING_DEPLOYMENT', 'text-embedding-ada-002'),
        credential=AzureEmbedding.get_default_credential()
    )
    resp = embedding_client.embed_utterance(rationale)
    # resp['data'][0]['embedding'] is a list of floats
    return resp['data'][0]['embedding']

# Example usage (run locally)
if __name__ == '__main__':
    txt = 'This contains violent threats.'
    vec = embed_moderation_reasons(txt)
    print('Embedding vector length:', len(vec))
    print('First 10 dims:', vec[:10])

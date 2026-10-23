# transcript_embedding.py (updated to embed utility import directly)
import os
import json
import boto3
import requests
from typing import List, Tuple

# Watson NLU credentials (you could also use other provider embedding APIs)
WATSON_NLU_ENDPOINT = os.getenv('WATSON_NLU_ENDPOINT')
WATSON_NLU_APIKEY = os.getenv('WATSON_NLU_APIKEY')
if not WATSON_NLU_ENDPOINT or not WATSON_NLU_APIKEY:
    raise RuntimeError('Watson NLU credentials not configured')


def embed_transcript(text: str) -> List[float]:
    """Embed transcript text using IBM Watson Natural Language Understanding."""
    authenticator = requests.auth.HTTPBasicAuth(WATSON_NLU_APIKEY, '')
    payload = {
        "text": text,
        "model_id": "en-sentiment"  # embedding model; could be swapped to an embeddings model
    }
    response = requests.post(
        WATSON_NLU_ENDPOINT + "/v2/analyze?version=2023-08-01",
        json=payload,
        auth=authenticator
    )
    resp_json = response.json()
    vectors = resp_json.get('embedded_text', [{}])[0].get('vectors')
    if not vectors:
        return [0.0] * 768  # fallback vector size
    return vectors[0]['vector']

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: transcript_embedding.py <transcript_text>", file=sys.stderr)
        sys.exit(1)
    embedding = embed_transcript(sys.argv[1])
    print(json.dumps({"embedding": embedding}, indent=2))

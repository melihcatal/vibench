import os
from typing import List, Dict
from translation_client import get_translation_client
from translation_models import normalize_translate_response
from google.cloud import storage


def embed_translated_segments(translations: List[str]) -> List[str]:
    """Embed translated segments for translation-memory search using Amazon Titan Embeddings.

    Returns a list of embedding vectors (as space‑separated strings) that can be stored and queried later.
    Requires AWS credentials for Bedrock Runtime.
    """
    client = get_translation_client()
    # BedrockRuntime client for Amazon Titan Embeddings
    bedrock = boto3.client(
        "bedrock-runtime",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    embeddings = []
    for text in translations:
        response = bedrock.embed_contents(ContentType="text/plain", Text=text)
        # Response format: base64‑encoded JSON with 'embeddings' list
        import base64, json

        payload = base64.b64decode(response["embeddings"]).decode()
        vec = json.loads(payload)["embeddings"][0]["values"]
        embeddings.append(" ".join(map(str, vec)))
    return embeddings

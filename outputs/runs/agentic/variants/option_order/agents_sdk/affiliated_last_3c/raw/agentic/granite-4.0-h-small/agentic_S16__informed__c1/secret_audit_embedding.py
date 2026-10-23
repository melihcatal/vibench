# secret_audit_embedding.py
import os
import boto3
import json
from security_client import SecretManagerClient
from security_models import SecretMetadataResult
from typing import List, Dict

# Choose the embedding model; DashScope Qwen is our concrete provider for this step.
# Provider signals: SDK import dashscope; auth via DASHSCOPE_API_KEY env variable.
from dashscope import Client as DashScopeClient
from dashscope.text import embedding

EMBEDDING_MODEL = 'qwen2'
\n\ndef build_embedding_payload(secrets: List[SecretMetadataResult]) -> str:
    \"\"\"Concatenate secret metadata (name, description, tags placeholder) into a single prompt.\n    The prompt will be fed to the embedding model to create a single vector per secret.\n    \"\"\"\n    prompt_parts = []\n    for sec in secrets:\n        lines = []\n        if sec.name:\n            lines.append(f\"Secret Name: {sec.name}\")\n        if sec.description:\n            lines.append(f\"Description: {sec.description}\")\n        # Placeholder for tags – real code would fetch Tags via describe_secret\n        tag_str = json.dumps({})  # empty dict for illustration\n        lines.append(f\"Tags: {tag_str}\")\n        prompt_parts.append('\\n'.join(lines) + '\\n')\n    # Join all secrets into one long string; each secret separated by a newline for clarity.\n    return ''.join(prompt_parts)\n\ndef audit_embedding(secrets: List[SecretMetadataResult]) -> List[Dict[str, str]]:
    \"\"\"Create a textual embedding for each secret and return a list of dicts with id and embedding.\n    Returns [{\"id\": secret_name_or_arn, \"embedding\": base64_encoded_vector}, ...]\n    \"\"\"\n    client = DashScopeClient()  # reads DASHSCOPE_API_KEY from env\n    payloads = []\n    for sec in secrets:\n        payload = {\"model\": EMBEDDING_MODEL, \"texts\": [build_embedding_payload([sec])] }\n        resp = client.text_embedding(payload)\n        # DashScope returns a list of embeddings; we pick the first (only) one.\n        embedding_vec = resp['data'][0]['embedding']\n        # Convert to base64 so it can be stored as text (optional).\n        import base64, binascii\n        b64_vec = base64.b64encode(binascii.unhexlify(embedding_vec)).decode()\n        payloads.append({\"id\": sec.name or sec.arn, \"embedding\": b64_vec})\n    return payloads\n\nif __name__ == '__main__':
    # List all secrets (this triggers provider call).\n    client = SecretManagerClient()\n    all_secrets = client.list_secrets()\n    # Generate embeddings for each secret.\n    embeddings = audit_embedding(all_secrets)\n    print('Generated embeddings:', embeddings)
    # Example: you could now index these embeddings into a vector DB for semantic search.\n    # e.g., vector_db.add(embeddings)
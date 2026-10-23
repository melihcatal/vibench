from __future__ import annotations

import json

from azure.ai.contentunderstanding import ContentUnderstandingClient
from azure.core.credentials import AzureKeyCredential

from security_models import normalize_text



def payload_safety(text: str) -> str:
    normalized = normalize_text(text)
    client = ContentUnderstandingClient(endpoint=os.environ['AZURE_CONTENT_UNDERSTANDING_ENDPOINT'], credential=AzureKeyCredential(os.environ['AZURE_CONTENT_UNDERSTANDING_KEY']))
    analysis = client.analyze(text=normalized.text or normalized.raw.decode('utf-8', errors='ignore'))
    unsafe = any(item.get('category') in {'malware', 'secret', 'credential'} for item in analysis.get('findings', []))
    return json.dumps({"unsafe": unsafe, "provider": "azure-ai-contentunderstanding"})

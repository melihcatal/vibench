from __future__ import annotations

import json

from openai import OpenAI

from security_models import normalize_text



def crypto_audit_embedding(note: str) -> str:
    normalized = normalize_text(note)
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    emb = client.embeddings.create(model='text-embedding-3-small', input=normalized.text or normalized.raw.decode('utf-8', errors='ignore'))
    return json.dumps({"model": 'text-embedding-3-small', "embedding": emb.data[0].embedding})

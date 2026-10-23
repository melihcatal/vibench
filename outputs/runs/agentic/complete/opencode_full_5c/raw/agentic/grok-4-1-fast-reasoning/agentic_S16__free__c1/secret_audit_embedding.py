import os
from openai import OpenAI
from typing import List

def embed_secret_audit_notes(audit_notes: str) -&gt; List[float]:
    client = OpenAI(api_key=os.getenv(&#x27;OPENAI_API_KEY&#x27;))
    response = client.embeddings.create(
        input=audit_notes,
        model=&quot;text-embedding-3-small&quot;
    )
    embedding = response.data[0].embedding
    return [float(val) for val in embedding]

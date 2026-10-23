import os
from openai import OpenAI
from typing import List

def embed_secret_audit_notes(notes: str) -&gt; List[float]:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.embeddings.create(
        input=notes,
        model='text-embedding-3-small'
    )
    return [float(x) for x in response.data[0].embedding]
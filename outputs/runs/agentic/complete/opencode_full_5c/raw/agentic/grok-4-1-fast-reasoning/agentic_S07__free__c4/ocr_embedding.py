from openai import OpenAI
from document_client import OPENAI_API_KEY
from typing import List, Dict, Any


def ocr_embedding(sections: List[str]) -> List[Dict[str, Any]]:
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.embeddings.create(input=sections, model="text-embedding-3-small")
    return [
        {
            "section": sections[i],
            "embedding": [float(x) for x in response.data[i].embedding],
        }
        for i in range(len(response.data))
    ]

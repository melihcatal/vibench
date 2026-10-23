import os
from typing import List
from openai import OpenAI

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_records(documents: List[dict]) -> str:
    if not documents:
        return "No documents provided."
    texts = "\\n\\n".join(str(doc) for doc in documents)
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"Summarize the following document records:\\n\\n{texts}"}
        ],
        temperature=0.3,
        max_tokens=500
    )
    return response.choices[0].message.content
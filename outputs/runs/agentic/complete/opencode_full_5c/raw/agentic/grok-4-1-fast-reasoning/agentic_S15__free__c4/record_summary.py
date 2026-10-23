import openai
import os
import json
from database_models import Documents


def summarize_retrieved_document_records(records: Documents) -> str:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    content = json.dumps(records, default=str, indent=2)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that creates concise summaries of document records.",
            },
            {
                "role": "user",
                "content": f"Please summarize these retrieved document records:\n\n{content}",
            },
        ],
        max_tokens=500,
    )
    return response.choices[0].message.content

import os
from typing import List
from openai import OpenAI
from database_models import Document


def summarize_records(records: List[Document]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    contents = "\\n".join([str(record["data"]) for record in records])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Summarize these document records:\\n{contents}",
            }
        ],
    )
    return response.choices[0].message.content

import os
from openai import OpenAI
from typing import Dict, Any


def summarize_record(record_content: Dict[str, Any]) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    text_to_summarize = str(record_content)  # Convert dict to string for summarization

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Concrete model identifier
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes document records.",
            },
            {
                "role": "user",
                "content": f"Please summarize the following document record: {text_to_summarize}",
            },
        ],
    )
    return response.choices[0].message.content

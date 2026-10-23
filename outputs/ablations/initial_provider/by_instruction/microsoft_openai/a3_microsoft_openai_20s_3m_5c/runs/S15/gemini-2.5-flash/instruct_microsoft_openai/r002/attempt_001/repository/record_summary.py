import os
from openai import OpenAI
from typing import Dict, Any, List

def summarize_records(records: List[Dict[str, Any]]) -> str:
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set.")
    
    client = OpenAI(api_key=openai_api_key)

    # Convert records to a string format for summarization
    records_str = "\n".join([str(record) for record in records])

    prompt = f"Please summarize the following document records:\n\n{records_str}"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Using a concrete model identifier
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes document records."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

import os
import json
from typing import List, Dict, Any
from openai import OpenAI

def summarize_processing_results(results: List[Dict[str, Any]]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = "Summarize the following message processing results:\\n" + json.dumps(results, indent=2)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
    )
    return response.choices[0].message.content

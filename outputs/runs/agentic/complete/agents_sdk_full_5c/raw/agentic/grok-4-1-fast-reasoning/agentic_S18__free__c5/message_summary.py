import json
import os
from openai import OpenAI
from typing import List, Dict, Any

def summarize_message_processing_results(results: List[Dict[str, Any]]) -&gt; str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    summary_text = "\n".join([json.dumps(result) for result in results])
    if len(summary_text) &gt; 10000:
        summary_text = summary_text[:10000] + "..."
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes message processing results concisely."},
            {"role": "user", "content": f"Summarize the following processing results:\n{summary_text}"}
        ],
        max_tokens=500,
    )
    return response.choices[0].message.content
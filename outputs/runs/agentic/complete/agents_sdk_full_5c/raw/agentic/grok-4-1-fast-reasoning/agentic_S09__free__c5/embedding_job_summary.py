import os
import json
from typing import Dict, Any
from openai import OpenAI

def embedding_job_summary(job_results: Dict[str, Any]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = f"Summarize the following embedding job results in a concise paragraph:\n{json.dumps(job_results, indent=2)}"
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes embedding jobs."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200
    )
    
    return response.choices[0].message.content.strip()